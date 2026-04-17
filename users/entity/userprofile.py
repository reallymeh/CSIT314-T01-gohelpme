from dataclasses import dataclass
from database import connect_db
from typing import List

@dataclass
class UserProfile:
    """
    base class for user profiles
    """
    name: str
    access_level: int
    status: int
    description: str = " "

    @staticmethod
    def getProfile(profile_name:str) -> "UserProfile":
        conn, cur = connect_db()
        # check if need use ? to replace value
        res = cur.execute("SELECT * FROM user_profile WHERE name = ? ", (profile_name,))
        row = res.fetchone()
        name, access, status, description = row
        conn.close()


        return UserProfile(name, access, status, description) 



    @staticmethod
    def getUserProfiles() -> List["UserProfile"]:
        conn, cur = connect_db()
        rows = cur.execute("SELECT * FROM user_profile").fetchall()
        conn.close()

        return [
            UserProfile(name, access, status, description)
            for name, access, status, description in rows
        ]

    @staticmethod
    def userProfileExists(name: str) -> bool:
        conn, cur = connect_db()
        row = cur.execute(
            "SELECT 1 FROM user_profile WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))",
            (name,)
        ).fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def createUserProfile(name: str, access_level: int, status: int, description: str) -> bool:
        try:
            if not name:
                return False

            if UserProfile.userProfileExists(name):
                return False

            conn, cur = connect_db()
            cur.execute(
                "INSERT INTO user_profile (name, access, status, description) VALUES (?, ?, ?, ?)",
                (name, access_level, status, description)
            )
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Error:", e)
            return False
@staticmethod
def updateUserProfileDB(profile_id: str, new_name: str, new_access_level: int, new_description: str) -> bool:
    """
    Updates the profile name, access level, and description in the database.
    """
    conn, cur = connect_db()
    try:
        cur.execute(
            "UPDATE user_profile SET name = ?, access = ?, description = ? WHERE name = ?",
            (new_name, new_access_level, new_description, profile_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


@staticmethod
def suspendProfile(user_profile_name : str) -> bool:
    conn, cur = None, None

    try:
        conn, cur = connect_db()
        cur.execute("""
            UPDATE user_profile
            SET status = 0
            WHERE name = ?
    """, (user_profile_name,))
        
        conn.commit() 
        if cur.rowcount == 0: 
            return False
        else:
            return True
    
    except Exception:
        return False
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

