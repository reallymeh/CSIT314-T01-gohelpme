from dataclasses import dataclass
from database import connect_db
from typing import List


@dataclass
class Favourite:
    """
    Entity: Favourite
    Represents a donee's saved (favourited) FRA.
    Maps to the donee_favourite table.
    """
    id: int
    donee_email: str
    fraId: str
    saved_date: str
    '''These fields are not stored in the donee_favourite table but are included here for convenience when viewing/searching favourites.'''
    title: str = ""
    description: str = ""
    category: str = ""
    target_amount: int = 0
    collected_amount: int = 0
    start_date: str = ""
    end_date: str = ""
    view_count: int = 0
    status: int = 1
    location: str = ""
    created_by: str = ""

    """
    User Story #28 (Donee): As a Donee, I want to save a FRA to my favourite list so that I can decide on a donation later.
    """
    @staticmethod
    def saveFavourite(donee_email: str, fraId: str) -> bool:
        try:
            conn, cur = connect_db()
            cur.execute(
                "INSERT OR IGNORE INTO donee_favourite (donee_email, fraId) VALUES (?, ?)",
                (donee_email, fraId)
            )
            conn.commit()
            saved = cur.rowcount > 0
            conn.close()
            return saved
        except Exception as e:
            print(f"DB error saving favourite: {e}")
            return False

    @staticmethod
    def isFavourite(donee_email: str, fraId: str) -> bool:
        """Check whether an FRA is already in the donee's favourite list."""
        conn, cur = connect_db()
        row = cur.execute(
            "SELECT 1 FROM donee_favourite WHERE donee_email = ? AND fraId = ?",
            (donee_email, fraId)
        ).fetchone()
        conn.close()
        return row is not None


    '''Not a user story'''
    @staticmethod
    def removeFavourite(donee_email: str, fraId: str) -> bool:
        """
        User Story #3b (Donee): Remove a FRA from the favourite list.
        """
        try:
            conn, cur = connect_db()
            cur.execute(
                "DELETE FROM donee_favourite WHERE donee_email = ? AND fraId = ?",
                (donee_email, fraId)
            )
            conn.commit()
            removed = cur.rowcount > 0
            conn.close()
            return removed
        except Exception as e:
            print(f"DB error removing favourite: {e}")
            return False
    
    
    """
    User Story #29: As a Donee, I want to search for an active FRA in my favourite list by name so that I can find a specific FRA within the favourite list.
    """
    @staticmethod
    def searchFavourites(donee_email: str, name: str) -> List["Favourite"]:
        conn, cur = connect_db()
        cur.execute("""
            SELECT df.id, df.donee_email, df.fraId, df.saved_date,
                   f.title, f.description, f.category,
                   f.target_amount, f.collected_amount,
                   f.start_date, f.end_date, f.status, f.location
            FROM donee_favourite df
            JOIN fra f ON df.fraId = f.fraId
            WHERE df.donee_email = ?
              AND f.title LIKE ?
            ORDER BY df.saved_date DESC
        """, (donee_email, '%' + name + '%'))
        rows = cur.fetchall()
        conn.close()
        return [
            Favourite(
                id=r[0], donee_email=r[1], fraId=r[2], saved_date=r[3],
                title=r[4], description=r[5], category=r[6],
                target_amount=r[7], collected_amount=r[8],
                start_date=r[9], end_date=r[10], status=r[11], location=r[12]
            )
            for r in rows 
        ]


    """
    User Story #30: As a Donee, I want to view FRA in my favourite listso that I can view all FRA within the favourite list.
    """
    @staticmethod
    def viewFavourites(donee_email: str) -> List["Favourite"]:
        conn, cur = connect_db()
        cur.execute("""
            SELECT df.id, df.donee_email, df.fraId, df.saved_date,
                   f.title, f.description, f.category,
                   f.target_amount, f.collected_amount,
                   f.start_date, f.end_date, f.status, f.location
            FROM donee_favourite df
            JOIN fra f ON df.fraId = f.fraId
            WHERE df.donee_email = ?
            ORDER BY df.saved_date DESC
        """, (donee_email,))
        rows = cur.fetchall()
        conn.close()
        return [
            Favourite(
                id=r[0], donee_email=r[1], fraId=r[2], saved_date=r[3],
                title=r[4], description=r[5], category=r[6],
                target_amount=r[7], collected_amount=r[8],
                start_date=r[9], end_date=r[10], status=r[11], location=r[12]
            )
            for r in rows
        ]
    
    