import sqlite3

def init_db():
    conn = sqlite3.connect("gohelpme.db")
    cur = conn.cursor()

    # Create table for user profiles
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user_profile (\
         name TEXT PRIMARY KEY,\
         access INTEGER NOT NULL,\
         status INTEGER NOT NULL,\
         description TEXT NOT NULL\
        )"
    )

    # Create table for user account
    cur.execute(
    "CREATE TABLE IF NOT EXISTS user_account (\
     full_name TEXT NOT NULL,\
     email_address TEXT PRIMARY KEY,\
     phone_number TEXT NOT NULL,\
     address TEXT NOT NULL,\
     user_type TEXT NOT NULL,\
     account_status INTEGER NOT NULL,\
     password TEXT NOT NULL, \
     FOREIGN KEY (user_type) REFERENCES user_profile(name)\
    )"
    )

    # Create table for user profiles
    cur.execute(
        "CREATE TABLE IF NOT EXISTS fra_category (\
         name TEXT PRIMARY KEY,\
         description TEXT,\
         status INTEGER NOT NULL\
                    )"
    )

    # sample test data
    user_account_data = [
        ('John Doe', 'admin@email.com', '+65 9123 4567', '123 Example Street', 'admin', 1, 'password123'),
        ('John Doe', 'johndoe@email.com', '+65 9123 4567', '123 Example Street', 'donee', 1, 'password123'),
        ('Jane Smith', 'janesmith@email.com', '+65 9234 5678', '456 Example Avenue', 'fund raiser', 1, 'password123'),
        ('Bob Lee', 'boblee@email.com', '+65 9345 6789', '789 Example Road', 'platform manager', 1, 'password123')
    ]
    cur.executemany("INSERT OR IGNORE INTO user_account VALUES(?, ?, ?, ?, ?, ?, ?)", user_account_data)
    conn.commit()
    # Populate user_profile table

    user_profile_data = [
    ('user_admin', 1, 1, "Administrator with full access" ),
    ('platform_manager', 2, 1, "Manager responsible for platform operations" ),
    ('fund_raiser', 3, 1, "User who creates and manages fundraising campaigns" ),
    ('donee', 4, 1, "User who receives funds from fundraising campaigns" )
    ]
    cur.executemany("INSERT OR IGNORE INTO user_profile VALUES(?, ?, ?, ?)", user_profile_data)
    conn.commit()

    fra_category_data = [
        ('equipment', 'donation of equipment', 1),
        ('cash', 'cash donation', 1)
    ]
    cur.executemany("INSERT OR IGNORE INTO fra_category VALUES(?, ?, ?)", fra_category_data)
    conn.commit()
    
    cur.close()
    conn.close()

def connect_db():
    conn = sqlite3.connect("gohelpme.db")
    return conn, conn.cursor()


def delete_db():
    conn = sqlite3.connect("gohelpme.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM user_profile")
    conn.commit()
    conn.close()
    
