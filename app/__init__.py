# Global Imports
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .blueprints.user.models import db
from .blueprints.admin.models import db

# This will create and configure the app
def create_app(test_config=None):
    # creating the app instance
    app = Flask(__name__, instance_relative_config=True)


    if test_config is None:
         # This will ensure the instance folder exists. if it doesn't exist it will be created.
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # This will load the instance configuration from the config.py file
        # if it exist or create it if it doesn't exist when not testing.

        file_path = os.path.join('./instance', 'config.py')

        content_file_path = os.path.join('./','.copy_config.txt')

        if not os.path.exists(file_path):
            # create the file if it doesn't exist
            with open(file_path, 'w') as new_file:

                # Read the content of the .copy_config.txt file
                with open(content_file_path, 'r') as content_file:
                    content = content_file.read()

                    # write the content of the .copy_config.txt file to the config.py file
                    new_file.write(content)

        else:
            # if the files exists, it will read the content of the config.py file and compare it with the content of the .copy_config.txt file.

            with open(file_path, 'r') as new_file:
                config_file = new_file.read()
            with open(content_file_path, 'r') as content_file:
                content = content_file.read()
                if config_file != content:
                    # if the content of the config.py file doesn't match the content of the .copy_config.txt file, it will update the config.py file with the content of the .copy_config.txt file. Plese note that the server need to restart after updating the .copy_config.txt file
                    with open(file_path, 'w') as new_file:
                        new_file.write(content)

        # importing the config class
        from instance.config import Config
        # This method is used to load configuration values from a Python object and initializing apllication configuration.
        app.config.from_object(Config)
        # app.config.from_pyfile('config.py', silent=True)


    else:
        # if the app is in testing, it will load the default test configuration

        app.config.from_mapping(test_config)

    # initializing the database
    # db = SQLAlchemy()
    db.init_app(app)

    #  Importing the blueprints and the registering blueprints
    from .blueprints.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    from .blueprints.user.routes import user_bp
    app.register_blueprint(user_bp)


    # this will show the root directory of the app
    @app.route('/')
    # @app.route('/hello')
    def index():
        return render_template('index.html')
        # current_directory = os.getcwd()
        # # show = print(current_directory)
        # return current_directory

    return app
