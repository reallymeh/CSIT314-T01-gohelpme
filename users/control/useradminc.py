
from users.entity.useraccount import UserAccount
from users.entity.userprofile import UserProfile, updateUserProfile, suspendProfile
from users.entity.useraccount import UserAccount, getAccount

from dataclasses import dataclass
from typing import List

@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        return UserProfile.getUserProfiles()

class CreateUserProfileController:
    def createUserProfile(self, name: str, access_level: int, status: int, description: str) -> bool:
        return UserProfile.createUserProfile(name, access_level, status, description)

@dataclass
class UpdateUserProfileController:
    def updateUserProfile(self, user_profile_name: str, new_name: str, new_access_level: int, new_description: str) -> bool:
        if new_access_level < 1 or new_access_level > 4:
            print(f"Validation Error: Access level {new_access_level} is out of bounds (1-4).")
            return False
        return updateUserProfile(user_profile_name, new_name, new_access_level, new_description)

@dataclass
class UpdateUserAccountController:
    def updateUserAccount(self, email_address: str, updated_data: dict) -> bool:
        """
        Validates and applies account updates.
        updated_data keys: name, email, phone, address, userType, accountStatus, password (optional)
        Identified by email_address (primary key).
        """
        if not updated_data.get('name'):
            return False

        updated_user = UserAccount(
            full_name=updated_data.get('name'),
            email_address=updated_data.get('email', email_address),
            phone_number=updated_data.get('phone', ''),
            address=updated_data.get('address', ''),
            user_type=updated_data.get('userType', ''),
            account_status=int(updated_data.get('accountStatus', 1)),
            password=updated_data.get('password', '')  # empty string = don't update
        )

        return UserAccount.updateUserAccount(email_address, updated_user)

class SuspendUserProfileController:
    def suspendUserProfile(self, user_profile_name: str) -> bool:
        return suspendProfile(user_profile_name)

class ViewUserProfileController:
    def viewUserProfile(self, profile_name: str) -> UserProfile:
        return UserProfile.getProfile(profile_name)

class SearchUserProfileController:
    def search_profiles(self, query: str) -> List[UserProfile]:
        all_profiles = UserProfile.getUserProfiles()

        if not query or query.strip() == "":
            return all_profiles

        query = query.strip().lower()
        results = [
            p for p in all_profiles
            if query in p.name.lower() or
               (hasattr(p, 'description') and query in getattr(p, 'description', '').lower())
        ]
        return results

# BCE CONTROLLER: ViewUserAccountController
class ViewUserAccountController:
    def viewUserAccount(self, account_name: str) -> UserAccount | None:
        return getAccount(account_name)

# BCE CONTROLLER: SearchUserAccountController
class SearchUserAccountController:
    def searchUserAccounts(self, query: str) -> List[UserAccount]:
        return UserAccount.searchAccounts(query)

# BCE CONTROLLER: GetUserAccountController
class GetUserAccountController:
    def getUserAccount(self, email_address: str) -> UserAccount | None:
        return UserAccount.getAccountByEmail(email_address)

class CreateUserAccountController:
    def createUserAccount(self, full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str) -> bool:
        if not email_address or not password:
            return False
        return UserAccount.createUserAccount(full_name, email_address, phone_number, address, user_type, account_status, password)

# BCE CONTROLLER: SuspendUserAccountController
class SuspendUserAccountController:
    def suspendUserAccount(self, email_address: str) -> bool:
        return UserAccount.suspendAccount(email_address)
    
class LoginController:
    def login(self, email_address: str, password: str) -> bool:
        if not email_address or not password:
            return False
        return UserAccount.login(email_address, password)

    def getUserType(self, email_address: str) -> str | None:
        if not email_address:
            return None
        return UserAccount.getUserType(email_address)
