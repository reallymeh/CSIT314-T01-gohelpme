from users.entity.user import User
from users.entity.userprofile import UserProfile
from users.control.useradminc import DisplayUserProfileController, CreateUserProfileController 

from flask import Blueprint, render_template, request, redirect, url_for

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

# Create user profile
class CreateUserProfile: 
    def __init__(self): 
        self.controller = CreateUserProfileController()
    def clickCreate(self):  
        name = request.form['name'].strip()
        access_levels = int(request.form['access_level'])
        statuses = int(request.form['status'])
        descriptions = request.form['description']
        return self.controller.createUserProfile(name, access_levels, statuses, descriptions)
    def displayError(self):
        return render_template(
            'UserAdminCreateUserProfile.html',
            message='Profile already exists or could not be created.',
            message_type='error'
        )
    def displaySuccess(self):
        return render_template(
            'UserAdminCreateUserProfile.html',
            message='Profile created successfully.',
            message_type='success'
        )

create_profile = CreateUserProfile()

@admin_profiles_bp.route('/create_profile', methods=['GET'])
def show_create_profile():
    return render_template('UserAdminCreateUserProfile.html')

@admin_profiles_bp.route('/create_profile', methods=['POST'])
def create_user_profile():
    if create_profile.clickCreate():
        return create_profile.displaySuccess() 
    else:
        return create_profile.displayError()
