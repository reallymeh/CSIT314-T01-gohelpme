from dataclasses import dataclass
from database import connect_db

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
        "SELECT password FROM user_account WHERE email_address = ?",
        (email_address,)
     )
      result = cur.fetchone()
      conn.close()

      if result:
        stored_password = result[0]

        # compare passwords
        if stored_password == password:   # ⚠️ plain text (not secure)
            return True

      return False
    
    @staticmethod
    def updateUserAccount(user_id: str, user_data: 'UserAccount') -> bool:
        """
        Updates the user account in the database.
        """
        conn, cur = connect_db()
        try:
            cur.execute(
                """UPDATE user_account 
                SET full_name = ?, email_address = ?, phone_number = ?, address = ?, user_type = ?, account_status = ? 
                WHERE id = ?""",
                (user_data.full_name, user_data.email_address, user_data.phone_number,
                user_data.address, user_data.user_type, user_data.account_status, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error updating user account: {e}")
            return False
        finally:
            conn.close()
        

def getAccount(account_name: str) -> UserAccount | None:
    conn, cur = connect_db()
    result = cur.execute(
        "SELECT * FROM user_account WHERE full_name = ?", (account_name,)
    )
    row = result.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None
    return UserAccount(row[0], row[1], row[2], row[3], row[4], row[5], row[6])