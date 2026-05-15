# Entity imports (for type hints and asdict)
from users.entity.useraccount import UserAccount
from users.entity.userprofile import UserProfile

from users.control.useradminc import (
    CreateUserAccountController, DisplayUserProfileController,
    UpdateUserProfileController, UpdateUserAccountController,
    SuspendUserProfileController, CreateUserProfileController,
    ViewUserProfileController, SearchUserProfileController,
    ViewUserAccountController, 
    SearchUserAccountController, GetUserAccountController,
    SuspendUserAccountController
)

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from typing import List

# flask integration
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')


def get_admin_email():
    """Returns the logged-in admin's email from session, or None."""
    return session.get('email_address')


def require_admin_login():
    """Redirect to login if no session. Returns None when session is valid."""
    if not get_admin_email():
        return redirect(url_for('user.show_login'))
    return None


'''
User Story #3: As a user admin, I want to create user profile so that I can handle different types of user.
'''
# BCE BOUNDARY: ShowCreateUserProfilePage
@admin_profiles_bp.route('/create_profile', methods=['GET'])
def show_create_profile():
    guard = require_admin_login()
    if guard:
        return guard
    return render_template('user_admin/UserAdminCreateUserProfile.html')

# Create user profile
class CreateUserProfile:
    def __init__(self):
        self.controller = CreateUserProfileController()

    def clickCreate(self, name: str, access_level: int, status: int, description: str) -> bool:
        if self.controller.createUserProfile(name, access_level, status, description):
            return self.displaySuccess()
        else:
            return self.displayError()

    def displayError(self):
        return 'Failed to create profile. Please check the input and try again.'

    def displaySuccess(self):
        return 'Profile created successfully!'

create_profile = CreateUserProfile()

# BCE BOUNDARY: CreateUserProfile — POST /admin/create_profile
@admin_profiles_bp.route('/create_profile', methods=['POST'])
def create_user_profile():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    name = data.get('name', '').strip()
    access_level = int(data.get('access'))
    status = int(data.get('status'))
    description = data.get('description', '')
    if CreateUserProfileController().userProfileExists(name):
        return jsonify({"success": False, "message": "User profile already exists."}), 400
    message = create_profile.clickCreate(name, access_level, status, description)
    return jsonify({'message': message})


'''
User Story #4: As a user admin, I want to view user profile so that I can view the different types of user profiles.
'''
class ViewUserProfile:
    def __init__(self):
        self.controller = ViewUserProfileController()

    def viewUserProfile(self, profile_name: str):
        return self.controller.viewUserProfile(profile_name)

@admin_profiles_bp.route('/viewprofile/<string:user_profile_name>')
def user_profile(user_profile_name):
    guard = require_admin_login()
    if guard:
        return guard
    display_profile = ViewUserProfile()
    profile = display_profile.viewUserProfile(user_profile_name)
    return render_template('user_admin/UserAdminViewProfile.html', profile=profile)

@admin_profiles_bp.route('/api/profiles/<user_profile_name>', methods=['GET'])
def get_profile_api(user_profile_name):
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    display_profile = ViewUserProfile()
    profile = display_profile.viewUserProfile(user_profile_name)

    if profile:
        return jsonify({
            "success": True,
            "data": {
                "name": profile.name,
                "access_level": profile.access_level,
                "description": profile.description
            }
        }), 200
    else:
        return jsonify({"success": False, "error": "Profile not found"}), 404


'''
User Story #5: As a user admin, I want to update user profile so that I can make changes to user profile.
'''
# Update profile
@admin_profiles_bp.route('/updateprofile/<user_profile_name>', methods=['GET'])
def render_update_page(user_profile_name):
    guard = require_admin_login()
    if guard:
        return guard
    return render_template('user_admin/UserAdminUpdateProfile.html', user_profile_name=user_profile_name)

class UpdateUserProfile:
    def __init__(self):
        self.controller = UpdateUserProfileController()

    def updateUserProfile(self, user_profile_name: str, new_name: str, new_access_level: int, new_description: str) -> bool:
        return self.controller.updateUserProfile(user_profile_name, new_name, new_access_level, new_description)

@admin_profiles_bp.route('/api/profiles/<user_profile_name>', methods=['PUT'])
def update_profile_api(user_profile_name):
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    new_profile_type = data.get('profile_type')
    new_access_level = data.get('access_level')
    new_description = data.get('description', '')

    try:
        new_access_level = int(new_access_level)
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Access Level must be a number"}), 400

    if new_access_level < 1 or new_access_level > 4:
        return jsonify({"success": False, "error": "Access Level must be between 1 and 4"}), 400

    update_controller = UpdateUserProfile()
    success = update_controller.updateUserProfile(user_profile_name, new_profile_type, new_access_level, new_description)

    if success:
        return jsonify({"success": True, "message": f"Profile {user_profile_name} updated successfully"}), 200
    else:
        return jsonify({"success": False, "error": "Failed to update profile in database"}), 500


'''
User Story #6: As a user admin, I want to suspend a user profile so that I can maintain user access.
'''
class SuspendUserProfile:
    def __init__(self):
        self.controller = SuspendUserProfileController()

    def displaySuspendSuccess(self):
        return "Successfully suspended user!"

    def displaySuspendFail(self):
        return "Failed to suspend user!"

    def suspendUserProfile(self, user_profile_name: str):
        if self.controller.suspendUserProfile(user_profile_name):
            return self.displaySuspendSuccess()
        else:
            return self.displaySuspendFail()

# BCE BOUNDARY: SuspendUserProfile — POST /admin/suspend_user
@admin_profiles_bp.route('/suspend_user', methods=['POST'])
def suspend_user():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    user_profile_name = data.get('user_profile_name')
    message = SuspendUserProfile().suspendUserProfile(user_profile_name)
    return jsonify({'message': message})


'''
User Story #7: As a user admin, I want to search for user profile using a search bar so that I can search for a specific user profile.
'''
class SearchUserProfile:
    def __init__(self):
        self.controller = SearchUserProfileController()

    def search_profiles(self, query: str):
        return self.controller.search_profiles(query)

@admin_profiles_bp.route('/search_profiles', methods=['POST'])
def search_user_profiles():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    body = request.get_json() or {}
    query = body.get('name', '').strip().lower()
    boundary = SearchUserProfile()
    results = boundary.search_profiles(query)
    data = [{"name": p.name, "description": getattr(p, 'description', '')} for p in results]
    if not data:
        return jsonify({"data": [], "message": "No profiles found."})
    return jsonify({"data": data})


'''
User Story #8: As a user admin, I want to create user account so that new users can access the platform.
'''
@admin_profiles_bp.route('/create_account', methods=['GET'])
def show_create_account():
    guard = require_admin_login()
    if guard:
        return guard
    return render_template('user_admin/UserAdminCreateUserAccount.html')

class CreateUserAccount:
    def __init__(self):
        self.controller = CreateUserAccountController()

    def clickCreateAccount(self, full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str):
        result = self.controller.createUserAccount(full_name, email_address, phone_number, address, user_type, account_status, password)
        if result == "duplicate_email":
            return 'Email address already exists. Please use a different email.'
        if result:
            return self.displaySuccess()
        else:
            return self.displayError()

    def displayError(self):
        return 'Failed to create account. Please check the input and try again.'

    def displaySuccess(self):
        return 'Account created successfully!'
    
@admin_profiles_bp.route('/create_account', methods=['POST'])
def create_user_account_route():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    email = data.get('email', '').strip()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    hash_password = data.get('password', '').strip()
    account_status = data.get('account_status', '').strip()
    user_type = data.get('user_type', '').strip()
    
    create_account = CreateUserAccount()
    message = create_account.clickCreateAccount(name, email, phone, address, user_type, account_status, hash_password)
    success = message == create_account.displaySuccess()
    return jsonify({'success': success, 'message': message}), 200 if success else 400


'''
User Story #9: As a user admin, I want to view user account so that I can view the user's details.
'''
# BCE BOUNDARY: ViewUserAccount
class ViewUserAccount:
    def __init__(self):
        self.controller = ViewUserAccountController()

    def viewUserAccount(self, email_address: str) -> UserAccount | None:
        return self.controller.viewUserAccount(email_address)

@admin_profiles_bp.route('/viewaccount/<email_address>', methods=['GET'])
def view_account(email_address):
    guard = require_admin_login()
    if guard:
        return guard
    account = ViewUserAccount().viewUserAccount(email_address)
    if account is None:
        return redirect(url_for('admin_view_profile.user_account_list'))
    return render_template('user_admin/UserAdminViewAccount.html', account=account)

# BCE BOUNDARY: GetUserAccount — GET /admin/api/users/<email>
# Used by the update form to pre-fill current account data.
@admin_profiles_bp.route('/api/users/<path:user_id>', methods=['GET'])
def get_user_account_api(user_id):
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    account = GetUserAccount().getUserAccount(user_id)
    if account is None:
        return jsonify({"success": False, "message": "Account not found"}), 404
    return jsonify({
        "success": True,
        "data": {
            "full_name": account.full_name,
            "email_address": account.email_address,
            "phone_number": account.phone_number,
            "address": account.address,
            "user_type": account.user_type,
            "account_status": account.account_status
        }
    }), 200
    
    
'''
User Story #10: As a user admin, I want to update the user account so that I can ensure the information is the latest.
'''
# BCE BOUNDARY: UpdateUserAccount — render update form
# Passes user_id (email address) to the template so it can pre-fill and submit correctly.
@admin_profiles_bp.route('/updateaccount/<user_id>', methods=['GET'])
def render_update_account_page(user_id):
    guard = require_admin_login()
    if guard:
        return guard
    return render_template('user_admin/UserAdminUpdateAccount.html', user_id=user_id)

# BCE BOUNDARY: UpdateUserAccount
class UpdateUserAccount:
    def __init__(self):
        self.controller = UpdateUserAccountController()

    def updateUserAccount(self, email_address: str, data: dict) -> bool:
        return self.controller.updateUserAccount(email_address, data)

update_user_account = UpdateUserAccount()

# BCE BOUNDARY: UpdateUserAccount — PUT /admin/api/users/<email>
@admin_profiles_bp.route('/api/users/<path:user_id>', methods=['PUT'])
def update_user_account_api(user_id):
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    success = update_user_account.updateUserAccount(user_id, data)

    if success:
        return jsonify({"success": True, "message": f"Account {user_id} updated successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Failed to update account in database"}), 500


'''
User Story #11: As a user admin, I want to suspend a user account so that I can prevent unauthorised access.
'''
# BCE BOUNDARY: SuspendUserAccount
class SuspendUserAccount:
    def __init__(self):
        self.controller = SuspendUserAccountController()

    def displaySuspendSuccess(self):
        return "Account suspended successfully."

    def displaySuspendFail(self):
        return "Failed to suspend account."

    def suspendUserAccount(self, email_address: str) -> str:
        if self.controller.suspendUserAccount(email_address):
            return self.displaySuspendSuccess()
        else:
            return self.displaySuspendFail()
        
@admin_profiles_bp.route('/suspend_account', methods=['POST'])
def suspend_account():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    data = request.get_json()
    print("Suspend payload received:", data)
    email_address = data.get('email_address')
    print("Email to suspend:", email_address)
    message = SuspendUserAccount().suspendUserAccount(email_address)
    return jsonify({'message': message})


'''
User Story #12: As a user admin, I want to search a user account by name so that I can get a user's information quickly.
'''
# BCE BOUNDARY: SearchUserAccount
class SearchUserAccount:
    def __init__(self):
        self.controller = SearchUserAccountController()

    def searchUserAccounts(self, query: str) -> List[UserAccount]:
        return self.controller.searchUserAccounts(query)

# BCE BOUNDARY: SearchUserAccount — GET /admin/api/accounts?q=<query>
# Returns JSON list of matching accounts for the accounts page search.
@admin_profiles_bp.route('/api/accounts', methods=['GET'])
def search_user_accounts_api():
    guard = require_admin_login()
    if guard:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    query = request.args.get('q', '').strip()
    accounts = SearchUserAccount().searchUserAccounts(query)
    data = [
        {
            "full_name": a.full_name,
            "email_address": a.email_address,
            "user_type": a.user_type,
            "account_status": a.account_status
        }
        for a in accounts
    ]
    return jsonify(data), 200


class DisplayUserProfile:
    def __init__(self):
        self.controller = DisplayUserProfileController()

    def displayUserProfile(self) -> List[UserProfile]:
        return self.controller.displayUserProfile()

@admin_profiles_bp.route('/userprofile')
def user_profile_list():
    guard = require_admin_login()
    if guard:
        return guard
    display_profile = DisplayUserProfile()
    profiles = display_profile.displayUserProfile()
    message = request.args.get('message')
    return render_template('user_admin/UserAdminProfiles.html', profiles=profiles, message=message)


# BCE BOUNDARY: GetUserAccount (for pre-filling the update form)
class GetUserAccount:
    def __init__(self):
        self.controller = GetUserAccountController()

    def getUserAccount(self, email_address: str) -> UserAccount | None:
        return self.controller.getUserAccount(email_address)

# BCE BOUNDARY: SearchUserAccount — renders accounts page
@admin_profiles_bp.route('/useraccount', methods=['GET'])
def user_account_list():
    guard = require_admin_login()
    if guard:
        return guard
    return render_template('user_admin/UserAdminAccounts.html')
















