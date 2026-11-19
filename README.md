# Backend setup

1. Install and start PostgreSQL, then create the database:

   ```sql
   CREATE DATABASE db_lendora;
   ```

2. Copy `.env.example` to `.env` and set `DB_PASSWORD` to the password for your PostgreSQL user.
3. Install dependencies and initialize Django's authentication tables:

   ```powershell
   .\env\Scripts\python.exe -m pip install -r requirements.txt
   .\env\Scripts\python.exe manage.py migrate
   .\env\Scripts\python.exe manage.py runserver
   ```

Accounts use the custom `accounts.User` model with unique email addresses and a borrower or lender role. Create an administrator with `.\env\Scripts\python.exe manage.py createsuperuser` and sign in at `/admin/`. Administrators cannot register through public signup.

The authentication API is available at `/api/auth/signup/` and `/api/auth/login/`. Lenders and borrowers are sent to their respective starter portals after signing in.
