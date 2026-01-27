from flask import Flask

def create_app(config_name):
    app = Flask(__name__)

    app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite://app.db'


    return app