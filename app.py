from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from blueprints.login import login
from blueprints.sensors import sensors
from blueprints.actuators import actuators

USERS = {}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = "012345"

    login_manager = LoginManager()
    login_manager.login_view = "login.login_form"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id in USERS:
            return User(user_id)
        return None

    app.config["USERS_STORE"] = USERS
    app.config["USER_CLASS"] = User

    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(sensors, url_prefix='/')
    app.register_blueprint(actuators, url_prefix='/')

    @app.route('/', endpoint='home')
    def index():
        return render_template('home.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)