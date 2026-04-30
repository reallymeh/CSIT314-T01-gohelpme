from dataclasses import dataclass
from database import connect_db
from typing import List


@dataclass
class FRAView:
    id: int
    fraId: str
    viewer_email: str
    view_date: str

    @staticmethod
    def recordView(fraId: str, viewer_email: str, owner_email: str) -> bool:
      if not fraId or not viewer_email:
        print("❌ Missing data")
        return False


      if viewer_email == owner_email:
        return False

      try:
        conn, cur = connect_db()

        cur.execute("""
            INSERT INTO fra_view (fraId, user_email)
            VALUES (?, ?)
        """, (fraId, viewer_email))

        conn.commit()
        conn.close()

        print("✅ View recorded:", fraId, viewer_email)
        return True

      except Exception as e:
        print(f"DB error: {e}")
        return False 

    @staticmethod
    def getViewStatsByDateAndUser(fraId: str) -> List[dict]:
        """
        Get view count grouped by user and date
        """
        if not fraId:
            return []

        conn, cur = None, None

        try:
            conn, cur = connect_db()

            cur.execute("""
                SELECT user_email,
                       DATE(view_date) as view_date,
                       COUNT(*) as count
                FROM fra_view
                WHERE fraId = ?
                GROUP BY user_email, DATE(view_date)
                ORDER BY view_date DESC
            """, (fraId,))

            rows = cur.fetchall()

            return [
                {
                    "user_email": r[0],
                    "view_date": r[1],
                    "count": r[2]
                }
                for r in rows
            ]

        except Exception as e:
            print(f"[FRAView.getViewStats] DB error: {e}")
            return []

        finally:
            if conn:
                conn.close()