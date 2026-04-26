from dataclasses import dataclass
from database import connect_db
from typing import List

@dataclass
class FRACategory:
    category_name: str
    description: str
    status: int

    @staticmethod
    def createCategory(cat_name: str, description: str, status: int) -> bool:
        if FRACategory.checkCategoryExist(cat_name):
            return False
        else:
            conn, cur = connect_db()
            try:
                cur.execute(
                    "INSERT INTO fra_category (name, description, status) VALUES (?, ?, ?)",
                    (cat_name, description, status)
                )
                conn.commit()
                return True
            except Exception as e:
                print(e)
                conn.rollback()
                return False
            finally:
                cur.close()
                conn.close()

    @staticmethod
    def checkCategoryExist(name: str) -> bool:
        conn, cur = connect_db()
        cur.execute("SELECT 1 FROM fra_category WHERE name=? LIMIT 1", (name,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        return res is not None

    @staticmethod
    def getCategory(category_name: str) -> "FRACategory | None":
        conn, cur = connect_db()
        result = cur.execute(
            "SELECT * FROM fra_category WHERE name = ?", (category_name,)
        )
        row = result.fetchone()
        cur.close()
        conn.close()

        if row is None:
            return None
        return FRACategory(row[0], row[1], row[2])
    
    @staticmethod
    def getAllCategory() -> List["FRACategory"]:
        conn, cur = connect_db()
        try:
            result = cur.execute(
                "SELECT * FROM fra_category"
            )
            rows = result.fetchall()
            return [
            FRACategory(name, description, status)
            for name, description, status in rows
            ]

        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
    
    # check for backend for this user story
    @staticmethod
    def updateFRACategory(old_name: str, new_name: str, description: str, status: int) -> bool:
        conn, cur = connect_db()
        try:
            cur.execute(
                "UPDATE fra_category SET name = ?, description = ?, status = ? WHERE name = ?",
                (new_name, description, status, old_name)
            )
            conn.commit()
            if cur.rowcount == 0:
                return False
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
