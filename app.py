from flask import Flask, redirect
from database import init_db
from users.boundary.useradminb import admin_profiles_bp
from users.boundary.userb import user_bp
from users.boundary.fundraiserb import fundraiser_bp

def create_app():
    app = Flask(__name__)
    
    with app.app_context():
        init_db()
    app.register_blueprint(admin_profiles_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(fundraiser_bp)
    
    # Redirect to login page when accessing root URL
    @app.route('/')
    def index():
        return redirect('/admin/login')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)