# GoHelpMe — CSIT314 T01

A Flask-based fundraising activity (FRA) management platform supporting four user roles: User Admin, Platform Manager, Fund Raiser, and Donee.

---

## Setup

**Prerequisites:** Python 3.10+

```bash
pip install flask
python app.py
```

The app runs at `http://127.0.0.1:5000`. The SQLite database (`gohelpme.db`) is created and seeded automatically on first run.

---

## Test Accounts

| Role             | Email                    | Password      |
|------------------|--------------------------|---------------|
| User Admin       | `admin@email.com`        | `password123` |
| Platform Manager | `boblee@email.com`       | `password123` |
| Fund Raiser      | `janesmith@email.com`    | `password123` |
| Donee            | `johndoe@email.com`      | `password123` |

Login at: `http://127.0.0.1:5000/user/login`

---

## Portals

| Role             | Entry URL                              |
|------------------|----------------------------------------|
| User Admin       | `/admin/userprofile`                   |
| Platform Manager | `/manager/categories`                  |
| Fund Raiser      | `/fundraiser/homepage`                 |
| Donee            | `/donee/dashboard`                     |

All portals require an active login session and redirect to `/user/login` if unauthenticated.

---

## User Stories by Role

### User Admin
- Create, view, update, and suspend user profiles
- Create, view, update, and suspend user accounts
- Search user profiles and accounts

### Platform Manager
- Create, view, update, and suspend FRA categories
- Search FRA categories
- Generate daily, weekly, and monthly FRA view reports

### Fund Raiser
- Create, view, update, and suspend Fundraising Activities (FRAs)
- Search FRAs
- View FRA view counts and shortlist counts
- View and search completed FRA history

### Donee
- View and search all active FRAs
- View individual FRA details
- Save and remove FRAs from a favourites list
- View and search favourites
- View and search donation history by category and date

---

## Project Structure

```
app.py                        # App factory and entry point
database.py                   # SQLite init, seed data, connection helpers
users/
  boundary/
    userb.py                  # Login / logout routes
    useradminb.py             # User Admin routes
    platform_managerb.py      # Platform Manager routes
    fundraiserb.py            # Fund Raiser routes
    doneeb.py                 # Donee routes
  control/
    userc.py                  # Login controller
    useradminc.py             # User Admin controllers
    platform_managerc.py      # Platform Manager controllers
    fundraiserc.py            # Fund Raiser controllers
    doneec.py                 # Donee controllers
  entity/
    useraccount.py
    userprofile.py
    fra.py
    fracategory.py
    favourite.py
    donationhistory.py
    fra_view.py
```

---

## Database Schema

| Table              | Purpose                                      |
|--------------------|----------------------------------------------|
| `user_profile`     | Role definitions (admin, fund raiser, etc.)  |
| `user_account`     | User login credentials and personal details  |
| `fra_category`     | FRA category definitions                     |
| `fra`              | Fundraising Activity records                 |
| `fra_view`         | View tracking per FRA per user               |
| `donee_favourite`  | Donee saved FRA list                         |
| `donation_history` | Donee donation records                       |
