
from users.entity.user import User
from users.entity.userprofile import UserProfile, updateUserProfile, suspendProfile
from users.entity.useraccount import UserAccount, getAccount

from users.entity.user import User
from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        # talk to entity 
        return UserProfile.getUserProfiles()

#Create user profile 
class CreateUserProfileController:
    def createUserProfile(self, name:str, access_level:int, status:int, description:str) -> bool:
        return UserProfile.createUserProfile(name, access_level, status, description)


@dataclass
class UpdateUserProfileController:
    def updateUserProfile(self, user_profile_name: str, new_name: str, new_access_level: int, new_description: str) -> bool:  # Added description
        if new_access_level < 1 or new_access_level > 4:
            print(f"Validation Error: Access level {new_access_level} is out of bounds (1-4).")
            return False
            
        return updateUserProfile(user_profile_name, new_name, new_access_level, new_description)  # Added description
    
@dataclass
class UpdateUserAccountController:
    def updateUserAccount(self, user_id: str, updated_data: dict) -> bool:

        if not updated_data.get('name') or not updated_data.get('email'):
            return False

        updated_user = User(
            user_id=user_id,
            name=updated_data.get('name'),
            email=updated_data.get('email'),
            phone=updated_data.get('phone', ''),
            address=updated_data.get('address', ''),
            user_type=updated_data.get('userType'),
            bio=updated_data.get('bio', '')
        )
        
        return User.updateUserAccount(user_id, updated_user)
    
class SuspendUserProfileController:
    def suspendUserProfile(self, user_profile_name:str) -> bool:
        return suspendProfile(user_profile_name)

class ViewUserProfileController:
    def viewUserProfile(self, profile_name:str) -> UserProfile:
        return UserProfile.getProfile(profile_name)

class SearchUserProfileController:
    def search_profiles(self, query: str) -> List[UserProfile]:
        all_profiles = UserProfile.getUserProfiles()
        
        if not query or query.strip() == "":
            return all_profiles
            
        query = query.strip().lower()
        
        # filter logic, checks name and description to match against query
        results = [
            p for p in all_profiles
            if query in p.name.lower() or 
               (hasattr(p, 'description') and query in getattr(p, 'description', '').lower())
        ]
        return results
# BCE CONTROLLER: ViewUserAccountController
# User Story: As a user admin, I want to view user account so that I can view the user's details
# Receives account_name from ViewUserAccount boundary
# Calls getAccount() from UserAccount entity
# Returns UserAccount object or None back to boundary
class ViewUserAccountController:
    def viewUserAccount(self, account_name: str) -> UserAccount | None:
        return getAccount(account_name)
class CreateUserAccountController:
    def createUserAccount(self, full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str) -> bool:
         # Basic validation
        if not email_address or not password:
            return False
        return UserAccount.createUserAccount(full_name, email_address, phone_number, address, user_type, account_status, password)

class LoginController:
    def login(self, email_address: str, password: str) -> bool:
            if not email_address or not password:
                return False
            return UserAccount.login(email_address, password)