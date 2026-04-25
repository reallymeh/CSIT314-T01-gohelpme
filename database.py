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

    # Create table for FRA
    cur.execute(
        "CREATE TABLE IF NOT EXISTS fra ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        fraId TEXT UNIQUE, \
        title TEXT NOT NULL, \
        description TEXT NOT NULL, \
        category TEXT NOT NULL, \
        target_amount INTEGER NOT NULL, \
        collected_amount INTEGER DEFAULT 0, \
        start_date TEXT NOT NULL, \
        end_date TEXT NOT NULL, \
        status INTEGER NOT NULL, \
        view_count INTEGER DEFAULT 0, \
        location TEXT NOT NULL, \
        created_by TEXT, \
        FOREIGN KEY (created_by) REFERENCES user_account(email_address)\
    )"
    )
    
    # sample test data
    user_account_data = [
        ('Alice Ang', 'admin1@email.com', '+65 9123 4567', '123 Example Street', 'admin', 1, 'password123'),
        ('Bob Lee', 'donee1@email.com', '+65 9123 4567', '123 Example Street', 'donee', 1, 'password123'),
        ('Jane Smith', 'fundraiser1@email.com', '+65 9234 5678', '456 Example Avenue', 'fund raiser', 1, 'password123'),
        ('John Doe', 'platformmanager1@email.com', '+65 9345 6789', '789 Example Road', 'platform manager', 1, 'password123')
    ]
    cur.executemany("INSERT OR IGNORE INTO user_account VALUES(?, ?, ?, ?, ?, ?, ?)", user_account_data)

    # Populate user_profile table

    user_profile_data = [
    ('user_admin', 1, 1, "Administrator with full access" ),
    ('platform_manager', 2, 1, "Manager responsible for platform operations" ),
    ('fund_raiser', 3, 1, "User who creates and manages fundraising campaigns" ),
    ('donee', 4, 1, "User who receives funds from fundraising campaigns" )
    ]
    cur.executemany("INSERT OR IGNORE INTO user_profile VALUES(?, ?, ?, ?)", user_profile_data)

    fra_data = [
    ("FRA001", "Education Fund 2026", "Support students with tuition fees", "Education", 10000, 4500,
        "2026-01-01", "2026-12-31", 1, 120, "Admiralty Link Singapore","janesmith@email.com"),
    ("FRA002", "Medical Aid Fund", "Help patients with hospital bills", "Medical", 20000, 12300,
        "2026-02-01", "2026-10-30", 1, 98, "Steven Road Singapore", "janesmith@email.com"),
    ("FRA003", "Charity Relief Fund", "Community support for families", "Charity", 5000, 5000,
        "2025-05-01","2025-12-31", 0, 210, "Bedok North Singapore", "janesmith@email.com")
    ]
    cur.executemany("""INSERT OR IGNORE INTO fra (fraId, title, description, category, target_amount, collected_amount,
    start_date, end_date, status, view_count, location, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, fra_data)    
    
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
    
