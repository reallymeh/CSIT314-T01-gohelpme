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

