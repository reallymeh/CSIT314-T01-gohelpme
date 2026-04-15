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

    cur.close()
    conn.close()

    return [UserProfile(name,access,status) for name, access, status in rows]

def suspendProfile(user_profile_name : str) -> bool:
    conn, cur = None, None

    try:
        conn, cur = connect_db()
        cur.execute("""
            UPDATE user_profile
            SET status = 0
            WHERE name = ?
    """, (user_profile_name,))
        
        conn.commit() # save changes
        if cur.rowcount == 0: # no rows updated
            return False
        else:
            return True
    
    except Exception:
        # can add error code if needed
        return False
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

