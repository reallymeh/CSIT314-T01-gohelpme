from users.entity.user import User
from users.entity.userprofile import UserProfile
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