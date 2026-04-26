from dataclasses import dataclass
from datetime import datetime
from database import connect_db
from typing import List
from flask import session

@dataclass
class FRA:
    """
    Entity: FRA
    Represents a single fundraising campaign in the system.
    """
    fraId: str
    title: str
    description: str
    category: str
    target_amount: int
    collected_amount: int
    start_date: str
    end_date: str
    status: int  # e.g., 1 for Active, 0 for Suspended/Closed
    view_count: int
    location: str

    '''Dashboard: Fund Raiser Home Page'''
    @staticmethod
    def get_all_fra():
        conn, cur = connect_db()

        cur.execute("""
            SELECT fraId, title, description, category,
                   target_amount, collected_amount,
                   start_date, end_date, status,
                   view_count, location
            FROM fra
        """)

        rows = cur.fetchall()
        conn.close()

        return rows
    
    
    '''
    User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
    '''
    @staticmethod
    def createFRA(title: str, description: str, category: str,
                target_amount: int, start_date: str, end_date: str,
                status: int, location: str):

        collected_amount = 0
        view_count = 0

        conn, cur = connect_db()

        created_by = session.get("email_address")

        cur.execute("""
            INSERT INTO fra (
                title, description, category,
                target_amount, collected_amount,
                start_date, end_date, status,
                view_count, location, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, category,
            target_amount, collected_amount,
            start_date, end_date, status,
            view_count, location,
            created_by
        ))

        new_id = cur.lastrowid
        fraId = f"FRA{new_id:03d}"

        cur.execute("""
            UPDATE fra
            SET fraId = ?
            WHERE id = ?
        """, (fraId, new_id))

        conn.commit()
        conn.close()

        return True
        
    '''
    User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
    '''
    @staticmethod
    def viewFRA(fraId: str):
        conn, cur = connect_db()

        cur.execute("SELECT * FROM fra WHERE fraId = ?", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            return {
                "fraId": row[1],
                "title": row[2],
                "description": row[3],
                "category": row[4],
                "target_amount": row[5],
                "collected_amount": row[6],
                "start_date": row[7],
                "end_date": row[8],
                "status": row[9],
                "view_count": row[10],
                "location": row[11],
            }

        return None
    
    
    '''
    User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
    '''
    @staticmethod
    def updateFRA(fraId, title, description, category,
                target_amount, start_date, end_date, location):

        conn, cur = connect_db()

        try:
            cur.execute("""
                UPDATE fra
                SET title = ?, description = ?, category = ?,
                    target_amount = ?, start_date = ?, end_date = ?,
                    location = ?
                WHERE fraId = ?
            """, (
                title, description, category,
                target_amount, start_date, end_date,
                location, fraId
            ))

            conn.commit()
            return True

        except Exception as e:
            print("DB UPDATE ERROR:", e)
            return False

        finally:
            conn.close()
            

    '''
    User Story #18: As a Fund Raiser, I want to suspend a FRA so that I can stop the fund raising activity.
    '''
    @staticmethod
    def suspendFRA(fraId):
        conn, cur = connect_db()

        try:
            cur.execute("""
                UPDATE fra
                SET status = 0
                WHERE fraId = ?
            """, (fraId,))

            conn.commit()

            return cur.rowcount > 0

        except Exception as e:
            print("SUSPEND ERROR:", e)
            return False

        finally:
            conn.close()
            

    '''
    User Story #19: As a Fund Raiser, I want to search a FRA so that I can manage and update specific FRA efficiently.
    '''
    @staticmethod
    def searchFRA(name):
        conn, cur = connect_db()

        cur.execute("""
            SELECT * FROM fra
            WHERE title LIKE ?
        """, ('%' + name + '%',))

        rows = cur.fetchall()
        conn.close()

        result = []

        for row in rows:
            result.append({
                "fraId": row[1],
                "title": row[2],
                "description": row[3],
                "category": row[4],
                "target_amount": row[5],
                "collected_amount": row[6],
                "start_date": row[7],
                "end_date": row[8],
                "status": row[9],
                "view_count": row[10],
                "location": row[11]
            })

        return result
<<<<<<< HEAD

    '''
    User Story # (Donee): Search all active FRAs by name. Only returns FRAs with status = 1 (active), unlike the fund raiser searchFRA.
    '''
    @staticmethod
    def searchActiveFRA(name: str) -> list:
        conn, cur = connect_db()
        cur.execute("""
            SELECT fraId, title, description, category,
                   target_amount, collected_amount,
                   start_date, end_date, status,
                   view_count, location
            FROM fra
            WHERE status = 1 AND title LIKE ?
        """, ('%' + name + '%',))
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "fraId": r[0], "title": r[1], "description": r[2],
                "category": r[3], "target_amount": r[4], "collected_amount": r[5],
                "start_date": r[6], "end_date": r[7], "status": r[8],
                "view_count": r[9], "location": r[10]
            }
            for r in rows
        ]
=======
    '''
    User Story #20: As a Fund Raiser, I want to view the number of views of a FRA so that I can analyze the view of a FRA and adjust my strategy to attract more donees.
    '''
    @staticmethod
    def getFRAViewCount(fraId):
        conn, cur = connect_db()

        cur.execute("SELECT view_count FROM fra WHERE fraId = ?", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            return row[0]

        return None
    '''
    User Story #21: As a Fund Raiser, I want to view the number of times a FRA is shortlisted so that I can know how many people are interested in this FRA.
    '''
    @staticmethod
    def getFRAShortlistCount(fraId):
        conn, cur = connect_db()
        ''' Assuming there is a "shortlist" table that tracks which FRA has been shortlisted by users'''
        cur.execute("SELECT COUNT(*) FROM shortlist WHERE fraId = ?", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            return row[0]

        return None
    ''' 
    User Story #22: As a Fund Raiser, I want to search history of completed FRA by service category and date period so that I can search for the past FRA that is completed.
    '''
    @staticmethod 
    def searchCompletedFRAHistory(category, start_date, end_date):
        conn, cur = connect_db()

        cur.execute("""
            SELECT * FROM fra
            WHERE LOWER(category) LIKE LOWER(?)
              AND end_date BETWEEN ? AND ?
              AND status = 0
        """, ('%' + category.strip() + '%', start_date, end_date))

        rows = cur.fetchall()
        conn.close()

        result = []

        for row in rows:
            result.append({
                "fraId": row[1],
                "title": row[2],
                "description": row[3],
                "category": row[4],
                "target_amount": row[5],
                "collected_amount": row[6],
                "start_date": row[7],
                "end_date": row[8],
                "status": row[9],
                "view_count": row[10],
                "location": row[11]
            })

        return result
    '''
    User Story #23: As a Fund Raiser, I want to view the history of completed FRA by service category and date period so that I can review how the past FRA has progressed.
    '''
    @staticmethod
    def viewCompletedFRA(fraId: str):
        conn, cur = connect_db()

        cur.execute("SELECT * FROM fra WHERE fraId = ? AND status = 0", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            return {
                "fraId": row[1],
                "title": row[2],
                "description": row[3],
                "category": row[4],
                "target_amount": row[5],
                "collected_amount": row[6],
                "start_date": row[7],
                "end_date": row[8],
                "status": row[9],
                "view_count": row[10],
                "location": row[11],
            }

        return None
    
>>>>>>> 2acc2e3859bce03fd26f507c17b304769ae660a2
