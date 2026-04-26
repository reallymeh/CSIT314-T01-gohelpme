from flask import Flask
from database import init_db
from users.boundary.useradminb import admin_profiles_bp
from users.boundary.platform_managerb import platform_manager_bp
from users.boundary.fundraiserb import fundraiser_bp
from users.boundary.userb import user_bp
from users.boundary.doneeb import donee_bp

def create_app():
    app = Flask(__name__)

    app.secret_key = "csit314_secret_key"
    
    with app.app_context():
        init_db()

    app.register_blueprint(admin_profiles_bp)
    app.register_blueprint(platform_manager_bp)
    app.register_blueprint(fundraiser_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(donee_bp)

    '''# Redirect to login page when accessing root URL
    @app.route('/')
    def index():
        return redirect('/admin/login')
    return app
    '''

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)