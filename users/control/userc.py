from users.entity.useraccount import UserAccount


class LoginController:
    def login(self, email_address: str, password: str) -> bool:
        if not email_address or not password:
            return False
        return UserAccount.login(email_address, password)

    def getUserType(self, email_address: str) -> str | None:
        if not email_address:
            return None
        return UserAccount.getUserType(email_address)
