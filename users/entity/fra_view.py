from dataclasses import dataclass
from database import connect_db
from typing import List

from datetime import date


@dataclass
class FRAView:
   id: int
   fraId: str
   viewer_email: str
   view_date: str
   fra_name: str
   fra_category: str

   @staticmethod
   def getDailyCategoryView() -> List["FRAView"]:
      conn, cur = connect_db()

      today = date.today()
      try:
         cur.execute('''
            SELECT fra_category, COUNT(*) AS total_view 
            FROM fra_view
            WHERE DATE(view_date) = DATE(?) 
            GROUP BY fra_category
            ''', (today,))
         rows = cur.fetchall()
         return [
            {  
                  "fra_category": r[0],
                  "count": r[1],
            }
            for r in rows
         ]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   @staticmethod
   def getDailyFRAView() -> int:
      conn, cur = connect_db()

      today = date.today()

      try:
         cur.execute('''
            SELECT COUNT(*) AS TOTAL_VIEW FROM fra_view
            WHERE DATE(view_date) = DATE(?)
         ''', (today,))

         row = cur.fetchone()
         return row[0] if row else 0

      except Exception as e:
         print(e)
      
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

   @staticmethod
   def getWeeklyCategoryViews() -> List[dict]:
      conn, cur = connect_db()

      # get current year, month, date
      today = date.today()
      # extract week number
      week_num = today.isocalendar().week
      year_num = str(today.year)

      try:
         cur.execute('''
            SELECT fra_category, COUNT(*) AS total_view 
            FROM fra_view
            WHERE strftime('%Y', view_date) = ?
            AND CAST(strftime('%W', view_date) AS INTEGER) + 1 = ?
            GROUP BY fra_category
            ''', (year_num, week_num,))
         rows = cur.fetchall()
         return [
            {  
                  "fra_category": r[0],
                  "count": r[1],
            }
            for r in rows
         ]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   @staticmethod
   def getWeeklyFRAViews() -> int:
      conn, cur = connect_db()

      today = date.today()
      # extract week number
      week_num = today.isocalendar().week
      year_num = str(today.year)

      try:
         cur.execute('''
            SELECT COUNT(*) 
            FROM fra_view
            WHERE strftime('%Y', view_date) = ?
            AND CAST(strftime('%W', view_date) AS INTEGER) + 1 = ?
        ''', (year_num, week_num))
         row = cur.fetchone()
         return row[0] if row else 0

      except Exception as e:
         print(e)
      
      finally:
         cur.close()
         conn.close()
   
   @staticmethod
   def getMonthlyCategoryViews() -> List[dict]:
      conn, cur = connect_db()

      # get current year, month, date
      today = date.today()
      year_num = str(today.year)
      month_num = today.month
      if month_num < 10:
         month_num = "0" + (str(month_num))
      else:
         month_num = str(month_num)
      try:
         cur.execute('''
            SELECT fra_category, COUNT(*) AS total_view 
            FROM fra_view
            WHERE strftime('%Y', view_date) = ?
            AND strftime('%m', view_date) = ?
            GROUP BY fra_category
            ''', (year_num, month_num,))
         rows = cur.fetchall()
         print(rows)
         return [
            {  
                  "fra_category": r[0],
                  "count": r[1],
            }
            for r in rows
         ]
      except Exception as e:
         print(e)
         return []
      finally:
         cur.close()
         conn.close()

   @staticmethod
   def getMonthlyFRAViews() -> int:
      conn, cur = connect_db()

      today = date.today()
      # extract week number
      year_num = str(today.year)
      month_num = today.month
      if month_num < 10:
         month_num = "0" + (str(month_num))
      else:
         month_num = str(month_num)

      try:
         cur.execute('''
            SELECT COUNT(*) 
            FROM fra_view
            WHERE strftime('%Y', view_date) = ?
            AND strftime('%m', view_date) = ?
        ''', (year_num, month_num))
         row = cur.fetchone()
         return row[0] if row else 0

      except Exception as e:
         print(e)
      finally:
         cur.close()
         conn.close()