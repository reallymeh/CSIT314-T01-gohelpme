from dataclasses import dataclass
from .userprofile import UserProfile
from database import connect_db

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

@dataclass
class UserAccount:
    """
    Base class for user accounts
    """
    user_id: str
    name: str
    email: str
    phone: str
    address: str
    user_type: str
    bio: str

@staticmethod
def updateUserAccount(user_id: str, user_data: UserAccount) -> bool:
    """
    Takes a User object and updates the corresponding record in the database.
    """
    conn, cur = connect_db()
    try:
        cur.execute(
            """UPDATE user_account 
               SET name = ?, email = ?, phone = ?, address = ?, user_type = ?, bio = ? 
               WHERE id = ?""",
            (user_data.name, user_data.email, user_data.phone, user_data.address,
             user_data.user_type, user_data.bio, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error updating user account: {e}")
        return False
    finally:
        conn.close()