from users.entity.user import User
from users.entity.userprofile import UserProfile
from users.control.useradminc import DisplayUserProfileController, SuspendUserProfileController

from flask import Blueprint, render_template, request, jsonify

from typing import List

class DisplayUserProfile:
    def __init__(self):
        self.controller = DisplayUserProfileController()

    def displayUserProfile(self) -> List[UserProfile]:
        return self.controller.displayUserProfile()

# flask integration for display user profiles
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')

@admin_profiles_bp.route('/userprofile') # url will be .../admin/userprofile
def user_profile_list():
    display_profile = DisplayUserProfile()
    profiles = display_profile.displayUserProfile()
    return render_template('UserAdminProfiles.html', profiles=profiles)

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
    print(data)
    user_profile_name = data.get('user_profile_name')
    message = SuspendUserProfile().suspendUserProfile(user_profile_name)

    return jsonify({'message': message})
