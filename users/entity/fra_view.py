from dataclasses import dataclass
from database import connect_db
from typing import List


@dataclass
class FRAView:
    id: int
    fraId: str
    viewer_email: str
    view_date: str
    fra_name: str
    fra_category: str

    @staticmethod
    def recordView(fraId: str, viewer_email: str, owner_email: str, fra_name: str, fra_category: str) -> bool:
     if not fraId or not viewer_email:
        return False

     if viewer_email == owner_email:
        return False

     try:
        conn, cur = connect_db()

        cur.execute("""
            INSERT OR IGNORE INTO fra_view 
            (fraId, user_email, fra_name, fra_category)
            VALUES (?, ?, ?, ?)
        """, (fraId, viewer_email, fra_name, fra_category))

        conn.commit()
        return True

     except Exception as e:
        print(e)
        return False
     finally:
        conn.close()

    @staticmethod
    def getViewStatsByDateAndUser(fraId: str) -> List[dict]:
     if not fraId:
        return []

     conn, cur = None, None

     try:
        conn, cur = connect_db()

        cur.execute("""
            SELECT user_email,
                   DATE(view_date),
                   COUNT(*),
                   fra_name,
                   fra_category
            FROM fra_view
            WHERE fraId = ?
            GROUP BY user_email, DATE(view_date), fra_name, fra_category
            ORDER BY DATE(view_date) DESC
        """, (fraId,))

        rows = cur.fetchall()   

        return [
            {  
                "user_email": r[0],
                "view_date": r[1],
                "count": r[2],
                "fra_name": r[3],
                "fra_category": r[4]
            }
            for r in rows
        ]

     except Exception as e:
        print(f"[FRAView.getViewStats] DB error: {e}")
        return []

     finally:
        if conn:
            conn.close()