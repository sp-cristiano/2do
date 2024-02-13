from app import create_app, db
from werkzeug.security import generate_password_hash
from .models import Admin
from app.global_functions import add_commit_close

def create_default_admin():
    app = create_app()
    # This function will populate the user table with default values
    with app.app_context():
        admin_password = app.config['DEFAULT_ADMIN_PASSWORD']
        admin_pin = app.config['DEFAULT_ADMIN_PIN']
        admin_email = app.config['MAIL_USERNAME']
        admin_email = admin_email.lower()
        admin_username = app.config['DEFAULT_ADMIN_USERNAME']
        admin_username = admin_username.lower()
        admin_name = app.config['DEFAULT_ADMIN_NAME']
        admin_name = admin_name.capitalize()
        admin_phone = app.config['DEFAULT_ADMIN_PHONE']
        admin_gender = app.config['DEFAULT_ADMIN_GENDER']

        # hashing the details of the default admin user.
        hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256', salt_length=16)
        hashed_pin = generate_password_hash(admin_pin, method='pbkdf2:sha256', salt_length=16)

        # this function will query the database and check if the table is empty
        def is_table_empty(table_cls):
            user = table_cls.query.first()
            return user

        # populate the table with default data if they are empty

        # User Admin table
        if is_table_empty(Admin) is None:

            default_user = Admin(name=admin_name, username=admin_username, email=admin_email, _password=hashed_password, phone=admin_phone, gender=admin_gender, _pin=hashed_pin)

            # this function will add, commit then close a connection when calling it and if there is an error it will rollback to the previous state.
            add_commit_close(db, default_user)
        else:
            pass