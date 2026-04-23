from dataclasses import dataclass
from database import connect_db


@dataclass
class FRACategory:
    category_name: str
    description: str

    @staticmethod
    def createCategory(cat_name:str, description:str) -> bool:
        if FRACategory.checkCategoryExist(cat_name):
            return False
        else:
            conn, cur = connect_db()
            try:
                cur.execute(
                    "INSERT INTO fra_category (name, description) VALUES (?, ?)",
                    (cat_name, description)
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
    def checkCategoryExist(name:str) -> bool:
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
        return FRACategory(row[0], row[1])
