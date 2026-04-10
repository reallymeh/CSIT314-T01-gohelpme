from users.entity.user import User
from users.entity.userprofile import UserProfile, getUserProfile
from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        # talk to entity 
        return getUserProfile()
