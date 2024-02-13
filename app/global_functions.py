from flask import current_app
# from werkzeug.security import generate_password_hash
# from app.blueprints.admin.models import Admin
from app import db, create_app

# this function will add, commit then close a connection when calling it and if there is an error it will rollback to the previous state.
def add_commit_close(db, *objects):
    # This wil obtain the current app instance
    app = current_app._get_current_object()
    with app.app_context():
        try:
            # Add objects to the session
            db.session.add_all(objects)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()



