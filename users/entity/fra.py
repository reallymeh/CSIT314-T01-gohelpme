from dataclasses import dataclass
from database import connect_db
from typing import List

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
    created_by: str  # email of the fund raiser who created this FRA
    
    
    """
    User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
    """
    @staticmethod
    def createFRA(title: str, description: str, category: str,
                target_amount: int, start_date: str, end_date: str,
                status: int, location: str, created_by: str) -> bool:

        collected_amount = 0
        view_count = 0

        conn, cur = connect_db()

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
        
    """
    User Story #16: As a Fund Raiser, I want to view a FRA so that I can know my fund raising progress.
    """
    @staticmethod
    def viewFRA(fraId: str) -> "FRA":
        conn, cur = connect_db()

        cur.execute("SELECT * FROM fra WHERE fraId = ?", (fraId,))
        row = cur.fetchone()

        conn.close()

        # row[0]=id, row[1]=fraId, row[2]=title, row[3]=description, row[4]=category,
        # row[5]=target_amount, row[6]=collected_amount, row[7]=start_date, row[8]=end_date,
        # row[9]=status, row[10]=view_count, row[11]=location, row[12]=created_by
        fra = FRA(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        return fra
        

    """
    User Story #17: As a Fund Raiser, I want to update a FRA so that I can show my current status and need.
    """
    @staticmethod
    def updateFRA(fraId: str, title: str, description: str, category: str,
                target_amount: int, start_date: str, end_date: str, location: str) -> bool:

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
            

    """
    User Story #18: As a Fund Raiser, I want to suspend a FRA so that I can stop the fund raising activity.
    """
    @staticmethod
    def suspendFRA(fraId: str) -> bool:
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
            

    """
    User Story #19: As a Fund Raiser, I want to search a FRA so that I can manage and update specific FRA efficiently.
    """
    @staticmethod
    def searchFRA(name: str) -> List["FRA"]:
        conn, cur = connect_db()

        cur.execute("""
            SELECT * FROM fra
            WHERE title LIKE ?
        """, ('%' + name + '%',))

        rows = cur.fetchall()
        conn.close()

        result = []
        for row in rows:
            # row[0]=id, row[1]=fraId, row[2]=title, row[3]=description, row[4]=category,
            # row[5]=target_amount, row[6]=collected_amount, row[7]=start_date, row[8]=end_date,
            # row[9]=status, row[10]=view_count, row[11]=location, row[12]=created_by
            fra = FRA(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            result.append(fra)
        return result

    
    """
    User Story #21: As a Fund Raiser, I want to view the number of times a FRA is shortlisted so that I can know how many people are interested in this FRA.
    """
    @staticmethod
    def getFRAShortlistCount(fraId):
        conn, cur = connect_db()
        """ Assuming there is a "favorite" table that tracks which FRA has been favorited by users"""
        cur.execute("SELECT COUNT(*) FROM donee_favourite WHERE fraId = ?", (fraId,))
        row = cur.fetchone()

        conn.close()

        return row[0]
    
    
    """ 
    User Story #22: As a Fund Raiser, I want to search history of completed FRA by service category and date period so that I can search for the past FRA that is completed.
    """

    @staticmethod 
    def searchCompletedFRAHistory(category, start_date, end_date)->list["FRA"]:
        conn, cur = connect_db()

        cur.execute("""
           SELECT * FROM fra
           WHERE status = 0
           AND (? = '' OR category = ?)
           AND (? = '' OR start_date >= ?)
           AND (? = '' OR end_date <= ?)
        """, (
               category, category,
               start_date, start_date,
               end_date, end_date
             ))

        rows = cur.fetchall()
        conn.close()

        result = []

        for row in rows:
            # row[0]=id, row[1]=fraId, row[2]=title, row[3]=description, row[4]=category,
            # row[5]=target_amount, row[6]=collected_amount, row[7]=start_date, row[8]=end_date,
            # row[9]=status, row[10]=view_count, row[11]=location, row[12]=created_by
            fra = FRA(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            result.append(fra)

        return result
    
    
    """
    User Story #23: As a Fund Raiser, I want to view the history of completed FRA by service category and date period so that I can review how the past FRA has progressed.
    """
    @staticmethod
    def viewCompletedFRA(fraId: str) -> "FRA":
        conn, cur = connect_db()

        cur.execute("SELECT * FROM fra WHERE fraId = ? AND status = 0", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            # row[0]=id, row[1]=fraId, row[2]=title, row[3]=description, row[4]=category,
            # row[5]=target_amount, row[6]=collected_amount, row[7]=start_date, row[8]=end_date,
            # row[9]=status, row[10]=view_count, row[11]=location, row[12]=created_by
            fra = FRA(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            return fra

        return None
    
    
    """
    User Story #26: Search all active FRAs by name. Only returns FRAs with status = 1 (active), unlike the fund raiser searchFRA.
    """
    @staticmethod
    def searchActiveFRA(name: str) -> List["FRA"]:
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
            FRA(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], None)
            for r in rows 
        ]
        
        
    """
    User Story #27 (Donee): As a Donee, I want to view an active FRA
    so that I can view existing FRA information that needs donation.
    """
    @staticmethod
    def viewActiveFRA(fraId: str) -> "FRA":
        conn, cur = connect_db()

        cur.execute("SELECT * FROM fra WHERE fraId = ? AND status = 1", (fraId,))
        row = cur.fetchone()

        conn.close()

        if row:
            # row[0]=id, row[1]=fraId, row[2]=title, row[3]=description, row[4]=category,
            # row[5]=target_amount, row[6]=collected_amount, row[7]=start_date, row[8]=end_date,
            # row[9]=status, row[10]=view_count, row[11]=location, row[12]=created_by
            return FRA(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])

        return None
    
    
    """
    Not specifically mentioned in user stories, but needed for the fund raiser and doneeto view the list of their FRAs and manage them.
    """
    @staticmethod
    def displayFRA() -> list["FRA"]:
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

        result = []
        for row in rows:
            fra =FRA(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], None)
            result.append(fra)
        return result
    
    
    @staticmethod
    def viewAllActiveFRA() -> List["FRA"]:
        conn, cur = connect_db()
        cur.execute("""
            SELECT fraId, title, description, category,
                   target_amount, collected_amount,
                   start_date, end_date, status,
                   view_count, location
            FROM fra
            WHERE status = 1
        """)
        rows = cur.fetchall()
        conn.close()
        return [
            FRA(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], None)
            for r in rows
        ]

    
    