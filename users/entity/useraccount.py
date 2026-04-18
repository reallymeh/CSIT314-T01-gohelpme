from dataclasses import dataclass
from database import connect_db

@dataclass
class UserAccount:
    """
    base class for user accounts
    """
    full_name: str
    email_address: str
    phone_number: str
    address: str
    user_type: str
    account_status: int
    password: str

def getAccount(account_name: str) -> UserAccount | None:
    conn, cur = connect_db()
    result = cur.execute(
        "SELECT * FROM user_account WHERE full_name = ?", (account_name,)
    )
    row = result.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None
    return UserAccount(row[0], row[1], row[2], row[3], row[4], row[5], row[6])