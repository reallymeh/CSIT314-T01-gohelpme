from users.entity.user import User
from users.entity.userprofile import UserProfile
from users.control.useradminc import DisplayUserProfileController, UpdateUserProfileController, UpdateUserAccountController

from flask import Blueprint, render_template, request, jsonify

from typing import List

class DisplayUserProfile:
    def __init__(self):
        self.controller = DisplayUserProfileController()

    def displayUserProfile(self) -> List[UserProfile]:
        return self.controller.displayUserProfile()

class UpdateUserProfile:
    def __init__(self):
        self.controller = UpdateUserProfileController()
        
    def updateUserProfile(self, profile_id: str, new_name: str, new_access_level: int) -> bool:
        return self.controller.updateUserProfile(profile_id, new_name, new_access_level)

class UpdateUserAccount:
    def __init__(self):
        self.controller = UpdateUserAccountController()
        
    def updateUser(self, user_id: str, data: dict) -> bool:
        return self.controller.updateUser(user_id, data)

# flask integration
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')

display_profile = DisplayUserProfile()

update_user_account = UpdateUserAccount()

@admin_profiles_bp.route('/userprofile') # url will be .../admin/userprofile
def user_profile_list():
    profiles = display_profile.displayUserProfile()
    return render_template('UserAdminProfiles.html', profiles=profiles)

@admin_profiles_bp.route('/updateprofile/<profile_id>', methods=['GET']) # url will be .../admin/updateprofile/<profile_id>
def render_update_page(profile_id):
    return render_template('UserAdminUpdateProfile.html', profile_id=profile_id)

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
