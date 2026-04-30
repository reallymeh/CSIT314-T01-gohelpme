from dataclasses import dataclass
from database import connect_db
from typing import List


@dataclass
class FRAView:
    """
    Entity: FRAView
    Represents a view record of a Fund Raising Activity (FRA).
    Maps to the fra_view table.
    """
    id: int
    fraId: str
    viewer_email: str
    view_date: str

    @staticmethod
    def recordView(fraId: str, viewer_email: str, owner_email: str) -> bool:
        """
        Record a view ONLY if:
        - viewer is not the fundraiser (owner)
        - viewer has not already viewed today
        """
        try:
            # 🚫 Do not count fundraiser viewing own FRA
            if viewer_email == owner_email:
                return False

            conn, cur = connect_db()

            # ✅ Check if this user already viewed today
            cur.execute("""
                SELECT 1 FROM fra_view
                WHERE fraId = ?
                AND user_email = ?
                AND DATE(view_date) = DATE('now')
            """, (fraId, viewer_email))

            if cur.fetchone():
                conn.close()
                return False  # already counted today

            # ✅ Insert new view
            cur.execute("""
                INSERT INTO fra_view (fraId, user_email)
                VALUES (?, ?)
            """, (fraId, viewer_email))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"DB error recording FRA view: {e}")
            return False

    @staticmethod
    def getViewStatsByDateAndUser(fraId: str) -> List[dict]:
        """
        Get view count grouped by user and date
        """
        try:
            conn, cur = connect_db()

            cur.execute("""
                SELECT user_email, DATE(view_date), COUNT(*)
                FROM fra_view
                WHERE fraId = ?
                GROUP BY user_email, DATE(view_date)
                ORDER BY DATE(view_date) DESC
            """, (fraId,))

            rows = cur.fetchall()
            conn.close()

            return [
                {
                    "user_email": r[0],
                    "view_date": r[1],
                    "count": r[2]
                }
                for r in rows
            ]

        except Exception as e:
            print(f"DB error: {e}")
            return []