from flask import Flask
from assessment.models import *

def create_app():
    app = Flask(__name__)
    app.config["ASSESSMENT_ROOT"] = 'assessment'
    app.config["ASSESSMENT_SEED_DATA"] = f'{app.config["ASSESSMENT_ROOT"]}/seed_data.json'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://assessment_user:assessment_pwd@database_server/assessment_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True

    db.init_app(app)
    return app