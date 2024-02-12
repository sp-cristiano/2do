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
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        hashed_pin = generate_password_hash(pin, method='pbkdf2:sha256', salt_length=16)
        admin_email = app.config['MAIL_USERNAME']

        def is_table_empty(table_cls):
            user = table_cls.query.first()
            return user

        # populate the table with default data if they are empty

        # User Admin table
        if is_table_empty(Admin) is None:
            default_user = Admin(username='admin', email=admin_email, password=hashed_password, user_role='admin', gender='male', pin=hashed_pin)

            add_commit_close(db, default_user)
        else:
            pass

    app.run(debug=True)