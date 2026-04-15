from dataclasses import dataclass
from database import connect_db
from typing import List

@dataclass
class UserProfile:
    """
    base class for user profiles
    """
    profile_name:str
    access_level:int
    status:int

def getUserProfile() -> List[UserProfile]:
    conn, cur = connect_db()
    result = cur.execute("SELECT * FROM user_profile")
    rows = result.fetchall()
    conn.close()

    return [UserProfile(name,access,status) for name, access, status in rows]

def updateUserProfileDB(profile_id: str, new_name: str, new_access_level: int) -> bool:
    """
    Updates the profile name and access level in the database.
    Does not touch the status field.
    """
    conn, cur = connect_db()
    try:
        cur.execute(
            "UPDATE user_profile SET name = ?, access = ? WHERE name = ?",
            (new_name, new_access_level, profile_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

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
    status: str
    bio: str

# --- NEW UPDATE FUNCTION ---
def updateUserAccountDB(user_id: str, user_data: UserAccount) -> bool:
    """
    Takes a User object and updates the corresponding record in the database.
    """
    conn, cur = connect_db()
    try:
        # Note: Adjust table name and columns to match your exact database schema
        cur.execute(
            """UPDATE user_account 
               SET name = ?, email = ?, phone = ?, address = ?, user_type = ?, status = ?, bio = ? 
               WHERE id = ?""",
            (user_data.name, user_data.email, user_data.phone, user_data.address,
             user_data.user_type, user_data.status, user_data.bio, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error updating user account: {e}")
        return False
    finally:
        conn.close()
