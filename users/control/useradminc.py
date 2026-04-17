from users.entity.user import User
from users.entity.userprofile import UserProfile, updateUserProfileDB, updateUserAccountDB, suspendProfile
from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        # talk to entity 
        return UserProfile.getUserProfiles()

#Create user profile 
class CreateUserProfileController:
    def createUserProfile(self, name:str, access_levels:int, statuses:int, descriptions:str) -> bool:
        return UserProfile.createUserProfile(name, access_levels, statuses, descriptions)
        return getUserProfile()

@dataclass
class UpdateUserProfileController:
    def updateUserProfile(self, profile_id: str, new_name: str, new_access_level: int) -> bool:
        if new_access_level < 1 or new_access_level > 4:
            print(f"Validation Error: Access level {new_access_level} is out of bounds (1-4).")
            return False
            
        return updateUserProfileDB(profile_id, new_name, new_access_level)

@dataclass
class UpdateUserAccountController:
    def updateUserAccount(self, user_id: str, updated_data: dict) -> bool:
        # 1. Validation check
        if not updated_data.get('name') or not updated_data.get('email'):
            return False
            
        # 2. Create the User entity object from the frontend payload
        updated_user = User(
            user_id=user_id,
            name=updated_data.get('name'),
            email=updated_data.get('email'),
            phone=updated_data.get('phone', ''),
            address=updated_data.get('address', ''),
            user_type=updated_data.get('userType'),
            bio=updated_data.get('bio', '')
        )
        
        return updateUserAccountDB(user_id, updated_user)
    
class SuspendUserProfileController:
    def suspendUserProfile(self, user_profile_name:str) -> bool:
        return suspendProfile(user_profile_name)

class ViewUserProfileController:
    def viewUserProfile(self, profile_name:str) -> UserProfile:
        return UserProfile.getProfile(profile_name)
