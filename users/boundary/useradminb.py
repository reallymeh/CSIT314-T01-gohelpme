from users.entity.user import User
from users.entity.userprofile import UserProfile
from users.control.useradminc import DisplayUserProfileController

from flask import Blueprint, render_template

from typing import List

class DisplayUserProfile:
    def __init__(self):
        self.controller = DisplayUserProfileController()

    def displayUserProfile(self) -> List[UserProfile]:
        return self.controller.displayUserProfile()

# flask integration
admin_profiles_bp = Blueprint('admin_view_profile', __name__, url_prefix='/admin')

display_profile = DisplayUserProfile()

@admin_profiles_bp.route('/userprofile') # url will be .../admin/userprofile
def user_profile_list():
    profiles = display_profile.displayUserProfile()
    return render_template('UserAdminProfiles.html', profiles=profiles)
