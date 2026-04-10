import sqlite3

def init_db():
    conn = sqlite3.connect("gohelpme.db")
    cur = conn.cursor()

    # Create table for user profiles
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user_profile (\
         name TEXT PRIMARY KEY,\
         access_level INTEGER NOT NULL,\
         status INTEGER NOT NULL\
        )"
    )

    # Populate user_profile table

    user_profile_data = [
    ('user admin', 1, 1 ),
    ('platform manager', 2, 0 ),
    ('fund raiser', 3, 0 ),
    ('donee', 4, 0 )
    ]
    cur.executemany("INSERT OR IGNORE INTO user_profile VALUES(?, ?, ?)", user_profile_data)

    conn.commit()
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
    