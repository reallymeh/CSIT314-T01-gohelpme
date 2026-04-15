from users.entity.user import User
from users.entity.userprofile import UserProfile, getUserProfile, suspendProfile
from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        # talk to entity 
        return getUserProfile()

class SuspendUserProfileController:
    def suspendUserProfile(self, user_profile_name:str) -> bool:
        return suspendProfile(user_profile_name)

