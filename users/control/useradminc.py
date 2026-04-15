from users.entity.user import User
from users.entity.userprofile import UserProfile, getUserProfile, updateUserProfileDB
from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        # talk to entity 
        return getUserProfile()

@dataclass
class UpdateUserProfileController:
    def updateUserProfile(self, profile_id: str, new_name: str, new_access_level: int) -> bool:
        if new_access_level < 1 or new_access_level > 4:
            print(f"Validation Error: Access level {new_access_level} is out of bounds (1-4).")
            return False
            
        return updateUserProfileDB(profile_id, new_name, new_access_level)
