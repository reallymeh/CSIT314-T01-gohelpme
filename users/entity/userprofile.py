from dataclasses import dataclass
from database import connect_db
from typing import List

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
                "INSERT INTO user_profile (name, access_level, status, description) VALUES (?, ?, ?, ?)",
                (name, access_level, status, description)
            )
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Error:", e)
            return False