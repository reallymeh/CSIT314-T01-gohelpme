from dataclasses import dataclass
from .userprofile import UserProfile

@dataclass
class User:
    """
    base class for each user account
    """
    first_name: str
    last_name: str
    username: str
    hash_password: str
    user_profile: UserProfile
