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
