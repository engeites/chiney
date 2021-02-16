
class Configuration(object):
    DEBUG = True
    SECRET_KEY = "top_secret_key"
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:19734682@localhost/chiney'
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
