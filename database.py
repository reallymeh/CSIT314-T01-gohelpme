import sqlite3

def init_db():
    conn = sqlite3.connect("gohelpme.db")
    cur = conn.cursor()

    # Create table for user profiles
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user_profile (\
         name TEXT PRIMARY KEY,\
         access_level INTEGER NOT NULL,\
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
        FOREIGN KEY (created_by) REFERENCES user_account(email_address), \
        FOREIGN KEY (category) REFERENCES fra_category(name) \
    )"
    )
    #Create table for fra_view
    cur.execute(
        "CREATE TABLE IF NOT EXISTS fra_view (\
         id INTEGER PRIMARY KEY AUTOINCREMENT,\
         fraId TEXT NOT NULL, \
         user_email TEXT NOT NULL,\
         view_date DATETIME DEFAULT CURRENT_TIMESTAMP, \
         fra_name TEXT NOT NULL,  \
         fra_category TEXT NOT NULL,  \
         FOREIGN KEY (fraId) REFERENCES fra(fraId),\
         FOREIGN KEY (user_email) REFERENCES user_account(email_address), \
         FOREIGN KEY (fra_name) REFERENCES fra(title),\
         FOREIGN KEY (fra_category) REFERENCES fra(category) \
        )"
    )
    # sample test data
    user_account_data = [
        ('Alice Tan', 'admin@email.com', '+65 9123 4567', '123 Example Street', 'admin', 1, 'password123'),
        ('John Doe', 'johndoe@email.com', '+65 9123 4567', '123 Example Street', 'donee', 1, 'password123'),
        ('Jane Smith', 'janesmith@email.com', '+65 9234 5678', '456 Example Avenue', 'fund raiser', 1, 'password123'),
        ('Bob Lee', 'boblee@email.com', '+65 9345 6789', '789 Example Road', 'platform manager', 1, 'password123')
    ]
    cur.executemany("INSERT OR IGNORE INTO user_account VALUES(?, ?, ?, ?, ?, ?, ?)", user_account_data)
    conn.commit()
    # Populate user_profile table

    user_profile_data = [
        ('user_admin',        1, 1, "Administrator with full access"),
        ('platform_manager',  2, 1, "Manager responsible for platform operations"),
        ('fund_raiser',       3, 1, "User who creates and manages fundraising campaigns"),
        ('donee',             4, 1, "User who receives funds from fundraising campaigns"),
        # suspended profile — for US #6 suspend/test
        ('volunteer',         5, 0, "Volunteer supporting fundraising events"),
    ]
    cur.executemany("INSERT OR IGNORE INTO user_profile VALUES(?, ?, ?, ?)", user_profile_data)
    conn.commit()

    # ── User Accounts ─────────────────────────────────────────────────────────
    # Passwords are plain-text for testing only.
    # Includes: 2 admins, 2 platform managers, 3 fundraisers, 3 donees, 1 suspended
    user_account_data = [
        # Admins — user_type must match role_redirects key "admin" in userb.py
        ('Alice Tan',       'admin@email.com',          '+65 9123 4567', '123 Admin Street, Singapore',        'admin',            1, 'password123'),
        ('Carol White',     'admin2@email.com',         '+65 9111 2222', '22 Admin Avenue, Singapore',         'admin',            1, 'password123'),
        # Platform Managers — must match "platform manager"
        ('Bob Lee',         'boblee@email.com',         '+65 9345 6789', '789 Manager Road, Singapore',        'platform manager', 1, 'password123'),
        ('Diana Prince',    'diana@email.com',          '+65 9222 3333', '45 Platform Lane, Singapore',        'platform manager', 1, 'password123'),
        # Fundraisers — must match "fund raiser"
        ('Jane Smith',      'janesmith@email.com',      '+65 9234 5678', '456 Fundraiser Avenue, Singapore',   'fund raiser',      1, 'password123'),
        ('Michael Chen',    'michael@email.com',        '+65 9444 5555', '88 Clementi Road, Singapore',        'fund raiser',      1, 'password123'),
        ('Sarah Lim',       'sarah@email.com',          '+65 9555 6666', '10 Orchard Boulevard, Singapore',    'fund raiser',      1, 'password123'),
        # Donees
        ('John Doe',        'johndoe@email.com',        '+65 9123 4567', '123 Donee Street, Singapore',        'donee',            1, 'password123'),
        ('Emily Ng',        'emily@email.com',          '+65 9666 7777', '5 Tampines Walk, Singapore',         'donee',            1, 'password123'),
        ('Kevin Tan',       'kevin@email.com',          '+65 9777 8888', '30 Bishan Ring Road, Singapore',     'donee',            1, 'password123'),
        # Suspended account — for US #11 suspend account test
        ('Tom Suspended',   'suspended@email.com',      '+65 9888 9999', '99 Suspended Road, Singapore',       'donee',            0, 'password123'),
    ]
    cur.executemany("INSERT OR IGNORE INTO user_account VALUES(?, ?, ?, ?, ?, ?, ?)", user_account_data)
    conn.commit()

    # ── FRA Categories ────────────────────────────────────────────────────────
    fra_category_data = [
        ('Education', 'support students, schools, tuition fees, learning materials, or educational programs', 1),
        ('Medical',   'help cover medical treatments, hospital bills, healthcare expenses, or emergency medical support', 1),
        ('Charity',   'assist individuals, families, or communities in need with basic necessities, shelter, food, or financial aid', 1),
        ('Animal',    'support animal shelters, rescue operations, veterinary care, and wildlife conservation', 1),
        # suspended category — for US #38 suspend category test
        ('Disaster',  'emergency relief for natural or man-made disasters affecting communities', 0),
    ]
    cur.executemany("INSERT OR IGNORE INTO fra_category VALUES(?, ?, ?)", fra_category_data)
    conn.commit()

    # ── FRA Records ───────────────────────────────────────────────────────────
    # status 1 = active, 0 = completed/suspended
    fra_data = [
        # Active FRAs (status=1) — for donee search/view, fundraiser manage
        ("FRA001", "Education Fund 2026",        "Support students with tuition fees and school supplies",           "Education", 10000,  4500, "2026-01-01", "2026-12-31", 1, 120, "Admiralty Link, Singapore",     "janesmith@email.com"),
        ("FRA002", "Medical Aid Fund",            "Help patients cover hospital bills and treatment costs",          "Medical",   20000, 12300, "2026-02-01", "2026-10-30", 1,  98, "Stevens Road, Singapore",       "janesmith@email.com"),
        ("FRA003", "Animal Shelter Support",      "Fund food and veterinary care for rescued animals",               "Animal",     8000,  2100, "2026-03-01", "2026-09-30", 1,  55, "Pasir Ris Drive, Singapore",    "michael@email.com"),
        ("FRA004", "Community Charity Drive",     "Provide basic necessities to low-income families",                "Charity",   15000,  7800, "2026-01-15", "2026-06-30", 1,  74, "Woodlands Avenue, Singapore",  "michael@email.com"),
        ("FRA005", "Student Bursary Fund",        "Award bursaries to financially disadvantaged students",           "Education",  5000,  1200, "2026-04-01", "2026-11-30", 1,  30, "Clementi Road, Singapore",      "sarah@email.com"),
        ("FRA006", "Cancer Treatment Aid",        "Cover chemotherapy and medication costs for cancer patients",     "Medical",   25000, 18000, "2026-01-01", "2026-08-31", 1, 140, "Novena, Singapore",             "sarah@email.com"),
        # Completed FRAs (status=0) — for fundraiser completed history (US #22, #23)
        ("FRA007", "Charity Relief Fund 2025",    "Community support for families in need",                          "Charity",    5000,  5000, "2025-05-01", "2025-12-31", 0, 210, "Bedok North, Singapore",        "janesmith@email.com"),
        ("FRA008", "Flood Disaster Relief",       "Aid families displaced by flash floods",                          "Charity",   12000, 12000, "2025-06-01", "2025-10-31", 0, 185, "Choa Chu Kang, Singapore",      "michael@email.com"),
        ("FRA009", "Eye Care Education Drive",    "Fund free eye screening and glasses for school children",         "Education",  3000,  3000, "2025-03-01", "2025-08-31", 0,  90, "Jurong West, Singapore",        "sarah@email.com"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO fra (fraId, title, description, category, target_amount, collected_amount, "
        "start_date, end_date, status, view_count, location, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        fra_data
    )
    conn.commit()

    # Donee: Favourite list 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS donee_favourite (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            donee_email TEXT    NOT NULL,
            fraId       TEXT    NOT NULL,
            saved_date  TEXT    NOT NULL DEFAULT (date('now')),
            UNIQUE(donee_email, fraId),
            FOREIGN KEY (donee_email) REFERENCES user_account(email_address),
            FOREIGN KEY (fraId)       REFERENCES fra(fraId)
        )
    """)

    # Donee: Donation history
    cur.execute("""
        CREATE TABLE IF NOT EXISTS donation_history (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            donee_email  TEXT    NOT NULL,
            fraId        TEXT    NOT NULL,
            fra_title    TEXT    NOT NULL,
            fra_category TEXT    NOT NULL,
            amount       REAL    NOT NULL,
            donation_date TEXT   NOT NULL,
            FOREIGN KEY (donee_email) REFERENCES user_account(email_address),
            FOREIGN KEY (fraId)       REFERENCES fra(fraId)
        )
    """)

    # ── Donee Favourites ──────────────────────────────────────────────────────
    # Covers US #21 (shortlist count), US #28-#30 (save/search/view favourites)
    donee_favourite_seed = [
        ("johndoe@email.com", "FRA001", "2026-01-10"),
        ("johndoe@email.com", "FRA002", "2026-02-05"),
        ("johndoe@email.com", "FRA004", "2026-03-20"),
        ("emily@email.com",   "FRA001", "2026-02-14"),
        ("emily@email.com",   "FRA003", "2026-03-01"),
        ("emily@email.com",   "FRA006", "2026-04-10"),
        ("kevin@email.com",   "FRA002", "2026-01-25"),
        ("kevin@email.com",   "FRA005", "2026-04-05"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO donee_favourite (donee_email, fraId, saved_date) VALUES (?, ?, ?)",
        donee_favourite_seed
    )

    # ── Donation History ──────────────────────────────────────────────────────
    # Multiple donees, categories, and date ranges — for US #31 (search) and US #32 (view all)
    donation_seed = [
        # johndoe
        ("johndoe@email.com", "FRA001", "Education Fund 2026",     "Education", 150.00, "2026-02-10"),
        ("johndoe@email.com", "FRA002", "Medical Aid Fund",         "Medical",   300.00, "2026-03-05"),
        ("johndoe@email.com", "FRA001", "Education Fund 2026",     "Education",  75.00, "2026-04-01"),
        ("johndoe@email.com", "FRA004", "Community Charity Drive",  "Charity",   200.00, "2026-04-20"),
        ("johndoe@email.com", "FRA007", "Charity Relief Fund 2025", "Charity",   100.00, "2025-11-15"),
        # emily
        ("emily@email.com",   "FRA001", "Education Fund 2026",     "Education",  50.00, "2026-03-12"),
        ("emily@email.com",   "FRA006", "Cancer Treatment Aid",     "Medical",   500.00, "2026-04-18"),
        ("emily@email.com",   "FRA003", "Animal Shelter Support",   "Animal",    120.00, "2026-05-02"),
        # kevin
        ("kevin@email.com",   "FRA002", "Medical Aid Fund",         "Medical",   250.00, "2026-02-28"),
        ("kevin@email.com",   "FRA005", "Student Bursary Fund",     "Education", 180.00, "2026-04-25"),
        ("kevin@email.com",   "FRA008", "Flood Disaster Relief",    "Charity",    80.00, "2025-08-10"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO donation_history "
        "(donee_email, fraId, fra_title, fra_category, amount, donation_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        donation_seed
    )

    conn.commit()

    # ── FRA View History ──────────────────────────────────────────────────────
    # Multiple viewers across Jan–May 2026 for daily/weekly/monthly report testing
    fra_view_seed = [
        # January 2026
        ("FRA001", "johndoe@email.com", "2026-01-05 10:00:00", "Education Fund 2026",    "Education"),
        ("FRA002", "johndoe@email.com", "2026-01-05 11:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA004", "emily@email.com",   "2026-01-06 09:00:00", "Community Charity Drive", "Charity"),
        ("FRA001", "emily@email.com",   "2026-01-12 09:30:00", "Education Fund 2026",    "Education"),
        ("FRA006", "kevin@email.com",   "2026-01-12 14:00:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA003", "johndoe@email.com", "2026-01-20 14:00:00", "Animal Shelter Support",  "Animal"),
        ("FRA002", "kevin@email.com",   "2026-01-20 15:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA005", "emily@email.com",   "2026-01-25 08:30:00", "Student Bursary Fund",    "Education"),
        # February 2026
        ("FRA001", "johndoe@email.com", "2026-02-03 08:00:00", "Education Fund 2026",    "Education"),
        ("FRA002", "johndoe@email.com", "2026-02-03 09:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA006", "emily@email.com",   "2026-02-03 10:00:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA004", "kevin@email.com",   "2026-02-10 11:00:00", "Community Charity Drive", "Charity"),
        ("FRA001", "kevin@email.com",   "2026-02-17 10:00:00", "Education Fund 2026",    "Education"),
        ("FRA003", "emily@email.com",   "2026-02-17 12:00:00", "Animal Shelter Support",  "Animal"),
        ("FRA002", "johndoe@email.com", "2026-02-24 16:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA005", "johndoe@email.com", "2026-02-24 17:00:00", "Student Bursary Fund",    "Education"),
        # March 2026
        ("FRA002", "johndoe@email.com", "2026-03-02 11:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA006", "kevin@email.com",   "2026-03-02 12:00:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA001", "emily@email.com",   "2026-03-09 09:00:00", "Education Fund 2026",    "Education"),
        ("FRA003", "johndoe@email.com", "2026-03-09 10:00:00", "Animal Shelter Support",  "Animal"),
        ("FRA004", "emily@email.com",   "2026-03-16 14:00:00", "Community Charity Drive", "Charity"),
        ("FRA001", "kevin@email.com",   "2026-03-23 08:30:00", "Education Fund 2026",    "Education"),
        ("FRA002", "emily@email.com",   "2026-03-23 09:30:00", "Medical Aid Fund",        "Medical"),
        ("FRA005", "kevin@email.com",   "2026-03-30 12:00:00", "Student Bursary Fund",    "Education"),
        ("FRA006", "johndoe@email.com", "2026-03-30 13:00:00", "Cancer Treatment Aid",    "Medical"),
        # April 2026
        ("FRA003", "johndoe@email.com", "2026-04-06 10:00:00", "Animal Shelter Support",  "Animal"),
        ("FRA001", "johndoe@email.com", "2026-04-06 11:00:00", "Education Fund 2026",    "Education"),
        ("FRA004", "kevin@email.com",   "2026-04-06 15:00:00", "Community Charity Drive", "Charity"),
        ("FRA006", "emily@email.com",   "2026-04-13 09:00:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA002", "johndoe@email.com", "2026-04-20 09:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA005", "emily@email.com",   "2026-04-20 10:00:00", "Student Bursary Fund",    "Education"),
        ("FRA001", "kevin@email.com",   "2026-04-27 10:00:00", "Education Fund 2026",    "Education"),
        ("FRA003", "emily@email.com",   "2026-04-27 11:00:00", "Animal Shelter Support",  "Animal"),
        # May 2026 (current month) — including same-day entries for daily report testing
        ("FRA001", "johndoe@email.com", "2026-05-04 08:00:00", "Education Fund 2026",    "Education"),
        ("FRA002", "emily@email.com",   "2026-05-04 09:00:00", "Medical Aid Fund",        "Medical"),
        ("FRA004", "kevin@email.com",   "2026-05-04 10:00:00", "Community Charity Drive", "Charity"),
        ("FRA006", "johndoe@email.com", "2026-05-04 11:00:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA003", "emily@email.com",   "2026-05-11 09:00:00", "Animal Shelter Support",  "Animal"),
        ("FRA001", "kevin@email.com",   "2026-05-11 10:00:00", "Education Fund 2026",    "Education"),
        ("FRA005", "johndoe@email.com", "2026-05-11 11:00:00", "Student Bursary Fund",    "Education"),
        ("FRA002", "kevin@email.com",   "2026-05-12 08:30:00", "Medical Aid Fund",        "Medical"),
        ("FRA006", "emily@email.com",   "2026-05-12 09:30:00", "Cancer Treatment Aid",    "Medical"),
        ("FRA001", "emily@email.com",   "2026-05-12 10:30:00", "Education Fund 2026",    "Education"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO fra_view (fraId, user_email, view_date, fra_name, fra_category) VALUES (?, ?, ?, ?, ?)",
        fra_view_seed
    )

    conn.commit()

    # ── ADD USER ACCOUNTS ──────────────────────────────────────────────────────
    # 50 unique donees
    donee_names = [
    'John Tan', 'Michael Lim', 'Sarah Lee', 'Emily Wong', 'Daniel Koh',
    'Jessica Tan', 'David Ong', 'Rachel Lim', 'Kevin Ng', 'Amanda Teo',
    'Ryan Chua', 'Sophia Goh', 'Ethan Yeo', 'Olivia Tan', 'Lucas Lim',
    'Grace Lee', 'Nathan Ong', 'Chloe Wong', 'Brandon Koh', 'Isabelle Ng',
    'Aaron Tan', 'Megan Lim', 'Jason Lee', 'Natalie Ong', 'Dylan Chua',
    'Charlotte Goh', 'Adam Teo', 'Hannah Wong', 'Benjamin Tan', 'Ella Lim',
    'Samuel Lee', 'Alicia Koh', 'Matthew Ng', 'Zoe Tan', 'Andrew Lim',
    'Victoria Ong', 'Joshua Chua', 'Samantha Goh', 'Caleb Teo', 'Madison Wong',
    'Isaac Tan', 'Lily Lim', 'Christopher Lee', 'Eva Ong', 'Nathaniel Chua',
    'Gabrielle Goh', 'Justin Teo', 'Claire Wong', 'Marcus Tan', 'Nicole Lim'
   ]

    # 50 unique fund raisers
    fundraiser_names = [
    'Evelyn Tan', 'Sean Lim', 'Melissa Lee', 'Jonathan Ong', 'Stephanie Chua',
    'Kenneth Goh', 'Vanessa Teo', 'Patrick Wong', 'Cynthia Tan', 'Ivan Lim',
    'Jasmine Lee', 'Terence Ong', 'Sharon Chua', 'Leonard Goh', 'Felicia Teo',
    'Wesley Wong', 'Janice Tan', 'Desmond Lim', 'Joanna Lee', 'Gerald Ong',
    'Tracy Chua', 'Nicholas Goh', 'Audrey Teo', 'Martin Wong', 'Belinda Tan',
    'Raymond Lim', 'Vivian Lee', 'Edwin Ong', 'Phoebe Chua', 'Dominic Goh',
    'Christine Teo', 'Alvin Wong', 'Denise Tan', 'Jeremy Lim', 'Selena Lee',
    'Marcus Ong', 'Naomi Chua', 'Darren Goh', 'Priscilla Teo', 'Keith Wong',
    'Sheryl Tan', 'Bryan Lim', 'Carmen Lee', 'Hugo Ong', 'Andrea Chua',
    'Trevor Goh', 'Monica Teo', 'Vincent Wong', 'Gloria Tan', 'Felix Lim'
   ]

   # Add donees
    for i, name in enumerate(donee_names, start=1):
      email = f"donee{i:03}@email.com"   # unique email
    
      user_account_data.append((
        name,
        email,
        f'+65 9000 {1000 + i}',
        f'{i} Donee Street',
        'donee',
        1,
        'password123'
      ))

   # Add fund raisers
    for i, name in enumerate(fundraiser_names, start=1):
      email = f"fundraiser{i:03}@email.com"   # unique email
    
      user_account_data.append((
        name,
        email,
        f'+65 8000 {1000 + i}',
        f'{i} Fundraiser Avenue',
        'fund raiser',
        1,
        'password123'
     ))
      
    cur.executemany("INSERT OR IGNORE INTO user_account VALUES(?, ?, ?, ?, ?, ?, ?)", user_account_data)
    conn.commit() 

    #── ADD USER PROFILES ──────────────────────────────────────────────────────
    profile_names = [f"profile_{i:03}" for i in range(1, 101)]  # Generate 100 unique profile names
    for i, name in enumerate(profile_names, start = 1):
        user_profile_data.append((
            profile_names[i-1],
            5,  # access_level
            1,  # status
            f"Description for {name}"
        ))
    cur.executemany("INSERT OR IGNORE INTO user_profile VALUES(?, ?, ?, ?)", user_profile_data)
    conn.commit()

    #── ADD FRA  ──────────────────────────────────────────────────────
    categories = ["Education", "Medical", "Animal", "Charity"]
    locations = [
    "Tampines, Singapore",
    "Yishun, Singapore",
    "Hougang, Singapore",
    "Jurong East, Singapore",
    "Bukit Panjang, Singapore",
    "Marine Parade, Singapore",
    "Bishan, Singapore",
    "Orchard, Singapore"
   ]

    emails = [
    "alex@email.com",
    "linda@email.com",
    "kevin@email.com",
    "olivia@email.com",
    "david@email.com",
    "emma@email.com"
 ]

    generated_fra_data = []

    for i in range(10, 101):
      category = categories[i % 4]

      title = f"{category} Support Fund {i}"
      description = f"Support community initiatives under {category.lower()} programs"

      target_amount = 5000 + (i * 300)
      current_amount = int(target_amount * 0.45)

      start_date = f"2026-{(i % 12) + 1:02d}-01"
      end_date = f"2026-{(i % 12) + 1:02d}-28"

      status = 1 if i <= 70 else 0
      donor_count = 20 + i

      location = locations[i % len(locations)]
      email = emails[i % len(emails)]

      generated_fra_data.append((
        f"FRA{i:03d}",
        title,
        description,
        category,
        target_amount,
        current_amount,
        start_date,
        end_date,
        status,
        donor_count,
        location,
        email
     ))
    cur.executemany(
        "INSERT OR IGNORE INTO fra (fraId, title, description, category, target_amount, collected_amount, "
        "start_date, end_date, status, view_count, location, created_by) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        generated_fra_data)
    conn.commit()

    #── ADD FRA CATEGORIES ──────────────────────────────────────────────────────
    for i in range(5, 101):
      category_name = f"Category_{i:03d}"
      description = (
        f"Description for {category_name} fundraising activities and community support"
    )
      status = 1 if i <= 80 else 0
      fra_category_data.append((
        category_name,
        description,
        status
    ))
    cur.executemany("INSERT OR IGNORE INTO fra_category VALUES (?, ?, ?)", fra_category_data)

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
    
