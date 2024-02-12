from app import create_app,db
from werkzeug.security import generate_password_hash
from app.blueprints.admin.models import Admin
from app.global_functions import add_commit_close


if __name__=='__main__':
    app = create_app()

# This function will populate the user table with default values
    with app.app_context():
        password = app.config['DEFAULT_ADMIN_PASSWORD']
        pin = app.config['DEFAULT_ADMIN_PIN']
        admin_email = app.config['MAIL_USERNAME']
        admin_email = admin_email.lower()
        admin_username = app.config['DEFAULT_ADMIN_USERNAME']
        admin_username = admin_username.lower()
        admin_name = app.config['DEFAULT_ADMIN_NAME']
        admin_name = admin_name.capitalize()
        admin_phone = app.config['DEFAULT_ADMIN_PHONE']
        admin_gender = app.config['DEFAULT_ADMIN_GENDER']

        # hashing the details of the default admin user.
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        hashed_pin = generate_password_hash(pin, method='pbkdf2:sha256', salt_length=16)
        hashed_email = generate_password_hash(admin_email, method='pbkdf2:sha256', salt_length=16)
        # hashed_username = generate_password_hash(admin_username, method='pbkdf2:sha256', salt_length=16)
        # hashed_name = generate_password_hash(admin_name, method='pbkdf2:sha256', salt_length=16)
        hashed_phone = generate_password_hash(admin_phone, method='pbkdf2:sha256', salt_length=16)

        def is_table_empty(table_cls):
            user = table_cls.query.first()
            return user

        # populate the table with default data if they are empty

        # User Admin table
        if is_table_empty(Admin) is None:
            default_user = Admin(name=admin_name, username=admin_username, email=hashed_email, password=hashed_password, phone=hashed_phone, gender=admin_gender, pin=hashed_pin)

            add_commit_close(db, default_user)
        else:
            pass

    app.run(debug=True)