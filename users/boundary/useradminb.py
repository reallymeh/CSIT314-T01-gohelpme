from users.entity.useraccount import UserAccount
from users.entity.user import User
from users.entity.userprofile import UserProfile

from users.control.useradminc import CreateUserAccountController, DisplayUserProfileController, UpdateUserProfileController, UpdateUserAccountController\
,SuspendUserProfileController,CreateUserProfileController, ViewUserProfileController,SearchUserProfileController, ViewUserAccountController, LoginController



from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort


from typing import List

class DisplayUserProfile:
    def __init__(self):
        self.controller = DisplayUserProfileController()

    def displayUserProfile(self) -> List[UserProfile]:
        return self.controller.displayUserProfile()
    
class UpdateUserProfile:
    def __init__(self):
        self.controller = UpdateUserProfileController()
        
    def updateUserProfile(self, user_profile_name: str, new_name: str, new_access_level: int, new_description: str) -> bool:
        return self.controller.updateUserProfile(user_profile_name, new_name, new_access_level, new_description)

class UpdateUserAccount:
    def __init__(self):
        self.controller = UpdateUserAccountController()
        
    def updateUser(self, user_id: str, data: dict) -> bool:
        return self.controller.updateUser(user_id, data)

# flask integration
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')

update_user_account = UpdateUserAccount()


@admin_profiles_bp.route('/userprofile') # url will be .../admin/userprofile
def user_profile_list():
    display_profile = DisplayUserProfile()
    profiles = display_profile.displayUserProfile()
    return render_template('UserAdminProfiles.html', profiles=profiles)

# Create user profile
class CreateUserProfile: 
    def __init__(self): 
        self.controller = CreateUserProfileController()

    def clickCreate(self,name, access_levels, statuses, descriptions):  
       if self.controller.createUserProfile(name, access_levels, statuses, descriptions):
           return self.displaySuccess()
       else: 
            return self.displayError()
       
    def displayError(self):
        return 'Failed to create profile. Please check the input and try again.'
    
    def displaySuccess(self):
        return 'Profile created successfully!'

create_profile = CreateUserProfile()

@admin_profiles_bp.route('/create_profile', methods=['GET'])
def show_create_profile():
    return render_template('UserAdminCreateUserProfile.html')

@admin_profiles_bp.route('/create_profile', methods=['POST'])# url will be .../admin/create_profile
def create_user_profile():
    data = request.get_json()
    name = data.get('name', '').strip()
    access_level = int(data.get('access'))
    status = int(data.get('status'))
    description = data.get('description', '')
    if UserProfile.userProfileExists(name):
        return jsonify({
            "success": False,
            "message": "User profile already exists."
        }), 400
    message = create_profile.clickCreate(name, access_level, status, description)
    return jsonify({'message': message})

# Update profile 
@admin_profiles_bp.route('/updateprofile/<user_profile_name>', methods=['GET']) # url will be .../admin/updateprofile/<profile_id>
def render_update_page(user_profile_name):
    return render_template('UserAdminUpdateProfile.html', user_profile_name=user_profile_name)

@admin_profiles_bp.route('/updateaccount/<user_id>', methods=['GET']) # url will be .../admin/updateaccount/<user_id>
def render_update_account_page(user_id):
    return render_template('UserAdminUpdateAccount.html', user_id=user_id)

@admin_profiles_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user_account_api(user_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    # Boundary calls the Controller
    success = update_user_account.updateUser(user_id, data)
    
    if success:
        return jsonify({"success": True, "message": f"Account {user_id} updated successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Failed to update account in database"}), 500

@admin_profiles_bp.route('/api/profiles/<user_profile_name>', methods=['GET'])
def get_profile_api(user_profile_name):
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

@admin_profiles_bp.route('/api/profiles/<user_profile_name>', methods=['PUT'])
def update_profile_api(user_profile_name):
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    new_profile_type = data.get('profile_type')
    new_access_level = data.get('access_level')
    new_description = data.get('description', '')
    
    # Convert to integer
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
      
class SuspendUserProfile:
    def __init__(self):
        self.controller = SuspendUserProfileController()
    
    def displaySuspendSuccess(self):
        return "Succesfully suspend user!"
    
    def displaySuspendFail(self):
        return "Failed to suspend user!"

    def suspendUserProfile(self, user_profile_name:str):
        if self.controller.suspendUserProfile(user_profile_name):
            return self.displaySuspendSuccess()
        else:
            return self.displaySuspendFail()

@admin_profiles_bp.route('/suspend_user', methods=['POST'])
def suspend_user():
    data = request.get_json()
    user_profile_name = data.get('user_profile_name')
    message = SuspendUserProfile().suspendUserProfile(user_profile_name)

    return jsonify({'message': message})

class LogoutPage: 
    def logout(self):
        return 'You have logged out successfully!'

@admin_profiles_bp.route('/logout')
def logout():
    page = LogoutPage()
    message = page.logout()
    return redirect(url_for('user.homepage', message=message))


class ViewUserProfile:
    def __init__(self):
        self.controller = ViewUserProfileController()

    def viewUserProfile(self, profile_name:str) -> UserProfile:
        return self.controller.viewUserProfile(profile_name)
    
@admin_profiles_bp.route('/viewprofile/<string:user_profile_name>')
def user_profile(user_profile_name):
    display_profile = ViewUserProfile()

    profile = display_profile.viewUserProfile(user_profile_name)
  
    return render_template('UserAdminViewProfile.html', 
                           profile=profile
                           )


class SearchUserProfile:
    def __init__(self):
        self.controller = SearchUserProfileController()   

    def search_profiles(self, query: str):
        return self.controller.search_profiles(query)


@admin_profiles_bp.route('/search_profiles', methods=['GET'])
def search_user_profiles():
    query = request.args.get('q', '').strip().lower()
    
    boundary = SearchUserProfile()
    results = boundary.search_profiles(query)

    data = [{
        "name": p.name,
        "description": getattr(p, 'description', '')
    } for p in results]
    
    return jsonify(data)
# BCE BOUNDARY: SearchUserAccount
# BACKEND: Replace hardcoded return with actual search logic
# render_template passes accounts list from SearchUserAccountController
@admin_profiles_bp.route('/useraccount', methods=['GET'])
def user_account_list():
    return render_template('UserAdminAccounts.html')

# BCE BOUNDARY: ViewUserAccount
# User Story: As a user admin, I want to view user account so that I can view the user's details
# Sequence: User Admin clicks View → ViewUserAccount(Boundary) → ViewUserAccountController(Controller) → UserAccount(Entity)
class ViewUserAccount:
    def __init__(self):
        self.controller = ViewUserAccountController()

    # BCE BOUNDARY: displayViewResult()
    # called when controller returns UserAccount object
    def displayViewResult(self, account: UserAccount):
        return account

    # BCE BOUNDARY: displayViewFail()
    # called when controller returns None
    # redirects back to user accounts page
    def displayViewFail(self):
        return None

    def viewUserAccount(self, account_name: str) -> UserAccount | None:
        return self.controller.viewUserAccount(account_name)

# flask integration
@admin_profiles_bp.route('/viewaccount/<account_name>', methods=['GET'])
def view_account(account_name):
    account = ViewUserAccount().viewUserAccount(account_name)
    if account is None:
        # BCE BOUNDARY: displayViewFail()
        return redirect(url_for('admin_view_profile.user_account_list'))
    # BCE BOUNDARY: displayViewResult()
    return render_template('UserAdminViewAccount.html', account=account)

class CreateUserAccount:
    def __init__(self):
        self.controller = CreateUserAccountController()
    def clickCreateAccount(self,full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str):
        if self.controller.createUserAccount(full_name, email_address, phone_number, address, user_type, account_status, password):
            return self.displaySuccess()
        else: 
            return self.displayError()
        
    def displayError(self):
        return 'Failed to create account. Please check the input and try again.'
    
    def displaySuccess(self):
        return 'Account created successfully!'
    

@admin_profiles_bp.route('/create_account', methods=['GET'])
def show_create_account():
    return render_template('UserAdminCreateUserAccount.html')
@admin_profiles_bp.route('/create_account', methods=['POST'])
def create_user_account_route():
    data = request.get_json()
    email = data.get('email', '').strip()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    hash_password = data.get('password', '').strip()
    account_status = data.get('account_status', '').strip()
    user_type = data.get('user_type', '').strip()
    if UserAccount.userAccountExists(email):
        return jsonify({
            "success": False,
            "message": "User account already exists."
        }), 400
    message = CreateUserAccount().clickCreateAccount(name, email, phone, address, user_type, account_status, hash_password)
    return jsonify({'message': message})

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

@admin_profiles_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('UserAdminLogin.html')
@admin_profiles_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    success = LoginController().login(email, password)

    return jsonify({
        "success": success,
        "message": "Login successful! Welcome back." if success else "Login failed. Please check your email and password."
    })