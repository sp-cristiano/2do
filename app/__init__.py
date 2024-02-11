# Global Imports
import os
from flask import Flask
# from config import Config

# This will create and configure the app
def create_app(test_config=None):
    # creating the app instance
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY = 'this is not a good secret key don\'t forget to change it',
        DATABASE = os.path.join(app.instance_path, 'todo.sqlite'),
    )
    
    if test_config is None:
        # This will load the instance configuration from the config.py file 
        # if it exist or create it if it doesn't exist when not testing
        
        file_path = os.path.join('./app', 'config.py')
        if not os.path.exists(file_path):
            # create an empty file
            with open(file_path, 'w'):
                pass
        
        app.config.from_pyfile('config.py', silent=True)
    else:
        # if the config.py file doesn't exist or if the app is in testing it will load the default text_configuration
        
        app.config.from_mapping(test_config)
        
    # This will ensure the instance folder exists. if it doesn't exist it will be created.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # this will show a simple page that says hello 
    @app.route('/')
    @app.route('/hello')
    def hello():
        current_directory = os.getcwd()
        # show = print(current_directory)
        return current_directory
    
    return app
