import os
 
app_dir = os.path.abspath(os.path.dirname(__file__))
 
class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
 
#Flask-Mail configurations #

    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('iReporter@gmail.com'),
    MAIL_PASSWORD=os.environ.get('ireport123456')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
 
 
class DevelopementConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or  \
    #     'mysql+pymysql://root:pass@localhost/flask_app_db'
    pass
    
 
class TestingConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
    #                           'mysql+pymysql://root:pass@localhost/flask_app_db'  
    pass  
 
class ProductionConfig(BaseConfig):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or  \
    #     'mysql+pymysql://root:pass@localhost/flask_app_db'
    pass