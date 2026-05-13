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

    """
    User Story #31 (Donee): As a Donee, I want to search history of donation by
    FRA category and date period so that I can find a specific FRA I had donated.
    """
    @staticmethod
    def searchHistory(donee_email: str, category: str,
                      date_from: str, date_to: str) -> List["DonationHistory"]:
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
            DonationHistory(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            for r in rows
        ]

    """
    User Story #32 (Donee): As a Donee, I want to view the history of donation
    so that I can evaluate the impact of my donation and consider another donation.
    """
    @staticmethod
    def viewHistory(donee_email: str) -> List["DonationHistory"]:
        conn, cur = connect_db()
        cur.execute(
            """
            SELECT id, donee_email, fraId, fra_title, fra_category, amount, donation_date
            FROM donation_history
            WHERE donee_email = ?
            ORDER BY donation_date DESC
            """,
            (donee_email,)
        )
        rows = cur.fetchall()
        conn.close()
        return [
            DonationHistory(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            for r in rows
        ]

