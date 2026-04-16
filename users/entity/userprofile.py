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
          
def updateUserProfileDB(profile_id: str, new_name: str, new_access_level: int) -> bool:
    """
    Updates the profile name and access level in the database.
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

# shift to user.py
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

# shift to user.py, make it into @static method
def updateUserAccountDB(user_id: str, user_data: UserAccount) -> bool:
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

