from users.entity.user import User
from users.entity.userprofile import UserProfile
from users.control.useradminc import DisplayUserProfileController, UpdateUserProfileController

from flask import Blueprint, render_template

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

# flask integration
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')

display_profile = DisplayUserProfile()

@admin_profiles_bp.route('/userprofile') # url will be .../admin/userprofile
def user_profile_list():
    profiles = display_profile.displayUserProfile()
    return render_template('UserAdminProfiles.html', profiles=profiles)

@admin_profiles_bp.route('/updateprofile/<profile_id>', methods=['GET']) # url will be .../admin/updateprofile/<profile_id>
def render_update_page(profile_id):
    return render_template('UserAdminUpdateProfile.html', profile_id=profile_id)
