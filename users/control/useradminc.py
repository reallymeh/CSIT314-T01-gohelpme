
from users.entity.useraccount import UserAccount
from users.entity.userprofile import UserProfile
from users.entity.useraccount import UserAccount

from dataclasses import dataclass
from typing import List

'''
User Story #3: As a user admin, I want to create user profile so that I can handle different types of user.
'''
class CreateUserProfileController:
    def createUserProfile(self, name: str, access_level: int, status: int, description: str) -> bool:
        return UserProfile.createUserProfile(name, access_level, status, description)


'''
User Story #4: As a user admin, I want to view user profile so that I can view the different types of user profiles.
'''
class ViewUserProfileController:
    def viewUserProfile(self, profile_name: str) -> UserProfile:
        return UserProfile.getProfile(profile_name)
    

'''
User Story #5: As a user admin, I want to update user profile so that I can make changes to user profile.
'''
@dataclass
class UpdateUserProfileController:
    def updateUserProfile(self, user_profile_name: str, new_name: str, new_access_level: int, new_description: str) -> bool:
        if new_access_level < 1 or new_access_level > 4:
            print(f"Validation Error: Access level {new_access_level} is out of bounds (1-4).")
            return False
        return UserProfile.updateUserProfile(user_profile_name, new_name, new_access_level, new_description)


'''
User Story #6: As a user admin, I want to suspend a user profile so that I can maintain user access.
'''
class SuspendUserProfileController:
    def suspendUserProfile(self, user_profile_name: str) -> bool:
        return UserProfile.suspendProfile(user_profile_name)


'''
User Story #7: As a user admin, I want to search for user profile using a search bar so that I can search for a specific user profile.
'''
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
    
    
'''
User Story #8: As a user admin, I want to create user account so that new users can access the platform.
'''
class CreateUserAccountController:
    def createUserAccount(self, full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str) -> bool:
        if not email_address or not password:
            return False
        return UserAccount.createUserAccount(full_name, email_address, phone_number, address, user_type, account_status, password)


'''
User Story #9: As a user admin, I want to view user account so that I can view the user's details.
'''
# BCE CONTROLLER: ViewUserAccountController
class ViewUserAccountController:
    def viewUserAccount(self, email_address: str) -> UserAccount | None:
        return UserAccount.getAccount(email_address)


'''
User Story #10: As a user admin, I want to update the user account so that I can ensure the information is the latest.
'''
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


'''
User Story #11: As a user admin, I want to suspend a user account so that I can prevent unauthorised access.
'''
# BCE CONTROLLER: SuspendUserAccountController
class SuspendUserAccountController:
    def suspendUserAccount(self, email_address: str) -> bool:
        return UserAccount.suspendAccount(email_address)
    

'''
User Story #12: As a user admin, I want to search a user account by name so that I can get a user's information quickly.
'''
# BCE CONTROLLER: SearchUserAccountController
class SearchUserAccountController:
    def searchUserAccounts(self, query: str) -> List[UserAccount]:
        return UserAccount.searchAccounts(query)


@dataclass
class DisplayUserProfileController:
    def displayUserProfile(self) -> List[UserProfile]:
        return UserProfile.getUserProfiles()

# BCE CONTROLLER: GetUserAccountController
class GetUserAccountController:
    def getUserAccount(self, email_address: str) -> UserAccount | None:
        return UserAccount.getAccountByEmail(email_address)


