✅ FIRST TIME LOCAL DB SETUP (AUTH SERVICE)
________________________________________
✅ 1. Activate Virtual Environment
Windows
venv\Scripts\activate
________________________________________
✅ 2. Install Requirements
pip install -r requirements.txt
________________________________________
✅ 3. Set Flask App
Windows CMD
set FLASK_APP=run.py
Windows PowerShell
$env:FLASK_APP="run.py"
________________________________________
✅ 4. Initialize Migrations (ONLY FIRST TIME)
flask db init
This creates:
migrations/
folder.
ONLY RUN ONCE.
________________________________________
✅ 5. Create Migration
flask db migrate -m "auth 2026 initial models"
________________________________________
✅ 6. Apply Migration
flask db upgrade
This creates all tables:
•	users 
•	token_blocklist 
•	password_reset_tokens 
•	email_verification_tokens 
•	refresh_tokens 
•	user_sessions 
•	user_addresses 
•	otp_verifications 
•	password_history 
________________________________________
✅ 7. Run Server
flask run
OR
python run.py
________________________________________
✅ 8. Verify Local APIs
http://127.0.0.1:5000/
Expected:
{
  "status": "Auth service started successfully."
}
________________________________________
✅ AFTER MODEL CHANGES LATER
Whenever models change:
flask db migrate -m "describe changes"

flask db upgrade
________________________________________
✅ IF MIGRATION GETS MESSED UP (LOCAL ONLY)
DELETE:
migrations/
AND DELETE:
auth.db
Then rerun:
flask db init

flask db migrate -m "fresh setup"

flask db upgrade
ONLY for LOCAL development cleanup.
________________________________________
✅ FINAL GIT AFTER TESTING
git add .

git commit -m "AUTH 2026: initial production auth setup"

git push origin feature/auth-2026-final-temp

