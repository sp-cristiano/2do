from app import create_app
from app.blueprints.admin.admin_functions import create_default_admin

if __name__=='__main__':
    app = create_app()
    
    # this function will create default admin user
    create_default_admin()

    app.run(debug=True)