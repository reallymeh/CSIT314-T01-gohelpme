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

   """
    User Story #40: As a platform manager, I want to generate a daily report, so that I can analyze the total number of views of all FRA and each FRA category.
    """
   @staticmethod
   def getViewsGroupedByDayAndCategory() -> List[dict]:
      conn, cur = connect_db()
      try:
         cur.execute('''
            SELECT DATE(view_date) AS day, fra_category, COUNT(*) AS total_view
            FROM fra_view
            GROUP BY DATE(view_date), fra_category
            ORDER BY DATE(view_date)
         ''')
         rows = cur.fetchall()
         return [{"period": r[0], "fra_category": r[1], "count": r[2]} for r in rows]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   """
    User Story #41: As a platform manager, I want to generate a weekly report, so that I can analyze the total number of views of all FRA and each FRA category.
    """
   @staticmethod
   def getViewsGroupedByWeekAndCategory() -> List[dict]:
      conn, cur = connect_db()
      try:
         cur.execute('''
            SELECT strftime('%Y', view_date) AS year,
                   strftime('%W', view_date) AS week,
                   fra_category, COUNT(*) AS total_view
            FROM fra_view
            GROUP BY year, week, fra_category
            ORDER BY year, week
         ''')
         rows = cur.fetchall()
         return [{"period": f"{r[0]}-W{r[1]}", "fra_category": r[2], "count": r[3]} for r in rows]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   """
    User Story #42: As a platform manager, I want to generate a monthly report, so that I can analyze the total number of views of all FRA and each FRA category.
    """
   @staticmethod
   def getViewsGroupedByMonthAndCategory() -> List[dict]:
      conn, cur = connect_db()
      try:
         cur.execute('''
            SELECT strftime('%Y-%m', view_date) AS month, fra_category, COUNT(*) AS total_view
            FROM fra_view
            GROUP BY month, fra_category
            ORDER BY month
         ''')
         rows = cur.fetchall()
         return [{"period": r[0], "fra_category": r[1], "count": r[2]} for r in rows]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   @staticmethod
   def getAllCategoryViews() -> List[dict]:
      conn, cur = connect_db()
      try:
         cur.execute('''
            SELECT fra_category, COUNT(*) AS total_view
            FROM fra_view
            GROUP BY fra_category
            ORDER BY total_view DESC
         ''')
         rows = cur.fetchall()
         return [{"fra_category": r[0], "count": r[1]} for r in rows]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()
   
   '''
   User Story #20: As a Fund Raiser, I want to view the number of views of a FRA so that I can analyze the view of a FRA and adjust my strategy to attract more donees.
   '''
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

