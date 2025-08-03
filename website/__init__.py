from flask import Flask, request
from flask_mysqldb import MySQL
from flask_babel import Babel

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecret-key-123'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600 

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'abilityhire'

    # Babel configuration
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']

    babel = Babel(app)

    def get_locale():
        # Try to get locale from query parameter, then from Accept-Language header
        lang = request.args.get('lang')
        if lang and lang in app.config['BABEL_SUPPORTED_LOCALES']:
            return lang
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

    babel.locale_selector_func = get_locale

    mysql.init_app(app) 

    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app
