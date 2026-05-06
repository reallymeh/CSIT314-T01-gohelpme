from users.entity.user import User
from flask import Blueprint, render_template, request, jsonify, url_for, redirect, session
from users.control.userc import LoginController

# flask integration
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/homepage')
def homepage():
    message = request.args.get('message')
    return render_template('user/HomePage.html', message=message)

'''
User Story #13: As a user admin, I want to log in my user account so that I can access the platform.
'''
@user_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('user/UserLogin.html')

class LoginPage:
    def clickLogin(self, email, password):
        login_controller = LoginController()
        if login_controller.login(email, password):
            return self.displaySuccess()
        else:
            return self.displayError()

    def displayError(self):
        return 'Login failed. Please check your email and password and try again.'

    def displaySuccess(self):
        return 'Login successful! Welcome back.'

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    page = LoginPage()
    login_controller = LoginController()
    success = login_controller.login(email, password)
    message = page.displaySuccess() if success else page.displayError()
    user_type = login_controller.getUserType(email) if success else None
    normalized_user_type = user_type.strip().lower() if user_type else ""

    if success:
        # Store identity in Flask session so all portals can identify the user
        session['email_address'] = email
        session['user_type'] = user_type

    role_redirects = {
        "admin": url_for('admin_view_profile.user_profile_list', message=message),
        "platform manager": url_for('platform_manager.view_all_category', message=message),
        "fund raiser": url_for('fundraiser.homepage', message=message),
        "donee": url_for('donee.dashboard', message=message),
    }
    redirect_url = role_redirects.get(normalized_user_type, url_for('user.homepage', message=message))
    return jsonify({
        "success": success,
        "message": message,
        "redirect_url": redirect_url if success else None,
        "user_type": user_type if success else None
    })

'''
User Story #13: As a user admin, I want to log in my user account so that I can access the platform.
'''
class LogoutPage:
    def logout(self):
        return 'You have logged out successfully!'

@user_bp.route('/logout')
def logout():
    session.clear()
    page = LogoutPage()
    message = page.logout()
    return redirect(url_for('user.homepage', message=message))
