from dataclasses import dataclass
from database import connect_db
from typing import List


@dataclass
class DonationHistory:
    """
    Entity: DonationHistory
    Represents a single donation made by a donee to an FRA.
    Maps to the donation_history table.
    """
    id: int
    donee_email: str
    fraId: str
    fra_title: str
    fra_category: str
    amount: float
    donation_date: str

    '''
    User Story #6 (Donee): Search history of donation by FRA category and date period.
    User Story #7 (Donee): View all history of donation (no filters = all records).
    '''
    @staticmethod
    def searchHistory(donee_email: str, category: str,
                      date_from: str, date_to: str) -> List[dict]:
        """
        Filters donation records by donee_email.
        Optionally also filters by category and/or date range.
        All three filters are optional — omitting them returns the full history.
        """
        conn, cur = connect_db()

        sql = """
            SELECT id, donee_email, fraId, fra_title, fra_category, amount, donation_date
            FROM donation_history
            WHERE donee_email = ?
        """
        params: list = [donee_email]

        if category and category.strip():
            sql += " AND LOWER(fra_category) = LOWER(?)"
            params.append(category.strip())

        if date_from and date_from.strip():
            sql += " AND donation_date >= ?"
            params.append(date_from.strip())

        if date_to and date_to.strip():
            sql += " AND donation_date <= ?"
            params.append(date_to.strip())

        sql += " ORDER BY donation_date DESC"

        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0], "donee_email": r[1], "fraId": r[2],
                "fra_title": r[3], "fra_category": r[4],
                "amount": r[5], "donation_date": r[6]
            }
            for r in rows
        ]

    @staticmethod
    def getDistinctCategories(donee_email: str) -> List[str]:
        """Return the distinct FRA categories that appear in this donee's history."""
        conn, cur = connect_db()
        rows = cur.execute(
            "SELECT DISTINCT fra_category FROM donation_history "
            "WHERE donee_email = ? ORDER BY fra_category",
            (donee_email,)
        ).fetchall()
        conn.close()
        return [r[0] for r in rows]
