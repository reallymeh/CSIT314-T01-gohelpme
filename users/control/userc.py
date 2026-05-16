from users.entity.useraccount import UserAccount

'''
User Story #13: As a user admin, I want to log in my user account so that I can access the platform.
User Story #24: As a Fund Raiser, I want to log in my user account so that I can start a session.
User Story #33: As a Donee, I want to log in my user account so that I can start a session.
User Story #43: As a Platform Manager, I want to log in my user account so that I can start a session.
'''
class LoginController:
    def login(self, email_address: str, password: str) -> bool:
        if not email_address or not password:
            return False
        return UserAccount.login(email_address, password)

    def getUserType(self, email_address: str) -> str | None:
        if not email_address:
            return None
        return UserAccount.getUserType(email_address)
