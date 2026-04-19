from dataclasses import dataclass
from database import connect_db
from typing import List

@dataclass
class UserAccount:
    """
    base class for user accounts
    """
    full_name: str
    email_address: str
    phone_number: str
    address: str
    user_type: str
    account_status: int
    password: str

    # Create user account
    @staticmethod
    def createUserAccount(full_name: str, email_address: str, phone_number: str, address: str, user_type: str, account_status: int, password: str) -> bool:
        try:
            if not full_name or not email_address or not phone_number or not address or not user_type or not password:
                return False

            conn, cur = connect_db()
            cur.execute(
                "INSERT INTO user_account (full_name, email_address, phone_number, address, user_type, account_status, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (full_name, email_address, phone_number, address, user_type, account_status, password)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error creating user account: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def userAccountExists(email_address: str) -> bool:
        conn, cur = connect_db()
        row = cur.execute(
            "SELECT 1 FROM user_account WHERE LOWER(TRIM(email_address)) = LOWER(TRIM(?))",
            (email_address,)
        ).fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def login(email_address: str, password: str) -> bool:
        conn, cur = connect_db()
        cur.execute(
            "SELECT password FROM user_account WHERE email_address = ? AND account_status = 1",
            (email_address,)
        )
        result = cur.fetchone()
        conn.close()
        if result:
            if result[0] == password:   # plain text (not secure)
                return True
        return False

    @staticmethod
    def getUserType(email_address: str) -> str | None:
        conn, cur = connect_db()
        cur.execute(
            "SELECT user_type FROM user_account WHERE email_address = ? AND account_status = 1",
            (email_address,)
        )
        result = cur.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    @staticmethod
    def getAccountByEmail(email_address: str) -> 'UserAccount | None':
        """Fetch a single account by email address (primary key)."""
        conn, cur = connect_db()
        row = cur.execute(
            "SELECT full_name, email_address, phone_number, address, user_type, account_status, password "
            "FROM user_account WHERE email_address = ?",
            (email_address,)
        ).fetchone()
        cur.close()
        conn.close()
        if row is None:
            return None
        return UserAccount(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    @staticmethod
    def searchAccounts(query: str) -> List['UserAccount']:
        """Search accounts by full_name (case-insensitive partial match). Empty query returns all."""
        conn, cur = connect_db()
        if query and query.strip():
            cur.execute(
                "SELECT full_name, email_address, phone_number, address, user_type, account_status, password "
                "FROM user_account WHERE LOWER(full_name) LIKE ?",
                (f"%{query.strip().lower()}%",)
            )
        else:
            cur.execute(
                "SELECT full_name, email_address, phone_number, address, user_type, account_status, password "
                "FROM user_account"
            )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [UserAccount(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]

    @staticmethod
    def updateUserAccount(email_address: str, user_data: 'UserAccount') -> bool:
        """
        Updates the user account in the database, identified by email_address (primary key).
        Password is only updated when a non-empty value is supplied.
        """
        conn, cur = connect_db()
        try:
            if user_data.password:
                cur.execute(
                    """UPDATE user_account
                    SET full_name = ?, email_address = ?, phone_number = ?, address = ?,
                        user_type = ?, account_status = ?, password = ?
                    WHERE email_address = ?""",
                    (user_data.full_name, user_data.email_address, user_data.phone_number,
                     user_data.address, user_data.user_type, user_data.account_status,
                     user_data.password, email_address)
                )
            else:
                cur.execute(
                    """UPDATE user_account
                    SET full_name = ?, email_address = ?, phone_number = ?, address = ?,
                        user_type = ?, account_status = ?
                    WHERE email_address = ?""",
                    (user_data.full_name, user_data.email_address, user_data.phone_number,
                     user_data.address, user_data.user_type, user_data.account_status,
                     email_address)
                )
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Database error updating user account: {e}")
            return False
        finally:
            conn.close()


def getAccount(account_name: str) -> UserAccount | None:
    """Fetch account by full_name (used by ViewUserAccount)."""
    conn, cur = connect_db()
    row = cur.execute(
        "SELECT full_name, email_address, phone_number, address, user_type, account_status, password "
        "FROM user_account WHERE full_name = ?", (account_name,)
    ).fetchone()
    cur.close()
    conn.close()
    if row is None:
        return None
    return UserAccount(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
