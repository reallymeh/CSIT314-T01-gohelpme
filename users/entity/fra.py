from dataclasses import dataclass
from datetime import datetime
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
    targetAmount: int
    collectedAmount: int
    startDate: str
    endDate: str
    status: int  # e.g., 1 for Active, 0 for Suspended/Closed
    viewCount: int
    location: str

    '''Dashboard: Fund Raiser Home Page'''
    @staticmethod
    def get_all_fra():
        conn, cur = connect_db()

        cur.execute("""
            SELECT fraId, title, description, category,
                   targetAmount, collectedAmount,
                   startDate, endDate, status,
                   viewCount, location
            FROM fra
        """)

        rows = cur.fetchall()
        conn.close()

        return rows
    
    '''
    User Story #15: As a Fund Raiser, I want to create a FRA so that I can share my story and start receiving donations.
    '''
    @staticmethod
    def createFRA(fraId: str, title: str, description: str, category: str, targetAmount: int, collectedAmount: int, \
                    startDate: str, endDate: str, status: int, viewCount: int, location: str) -> bool:
        conn, cur = connect_db()

        cur.execute("""
            INSERT INTO fra (
                fraId, title, description, category,
                targetAmount, collectedAmount,
                startDate, endDate, status,
                viewCount, location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fraId, title, description, category, targetAmount,collectedAmount,
            startDate, endDate, status, viewCount, location))

        conn.commit()
        conn.close()

        return True
    
    