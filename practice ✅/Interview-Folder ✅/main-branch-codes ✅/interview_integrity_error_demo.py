# =====================================================
# File Name: interview_integrity_error_demo.py
# =====================================================

# =====================================================
# PURPOSE OF THIS FILE
# =====================================================
#
# This file is created for:
#
# ✅ Interview practice
# ✅ Understanding try-except
# ✅ Understanding IntegrityError
# ✅ Hands-on confidence building
# ✅ Runtime input testing
# ✅ VSCode local practice
#
# Real backend applications use this concept
# while inserting users into databases.
#
# Example:
# - Duplicate email registration
# - Duplicate username
# - Unique constraint violations
#
# =====================================================



# =====================================================
# STEP 1: IMPORT IntegrityError
# =====================================================

# SQLAlchemy provides IntegrityError
# for database constraint violations

from sqlalchemy.exc import IntegrityError



# =====================================================
# STEP 2: HARDCODED DATABASE SIMULATION
# =====================================================

# Imagine this list is our database table

existing_emails = [
    "raghu@gmail.com",
    "admin@gmail.com"
]



# =====================================================
# STEP 3: REGISTER USER FUNCTION
# =====================================================

def register_user(email):

    try:

        # -------------------------------------------------
        # CHECK DUPLICATE EMAIL
        # -------------------------------------------------

        # If email already exists,
        # simulate database IntegrityError

        if email in existing_emails:

            raise IntegrityError(
                statement=None,
                params=None,
                orig="UNIQUE constraint failed: email already exists"
            )



        # -------------------------------------------------
        # INSERT NEW USER
        # -------------------------------------------------

        # Simulating database insert operation

        existing_emails.append(email)



        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        print("\n✅ User Registered Successfully")
        print(f"Registered Email: {email}")



    except IntegrityError as error:

        # -------------------------------------------------
        # ERROR HANDLING BLOCK
        # -------------------------------------------------

        print("\n❌ IntegrityError Occurred")



        # Actual database-like error

        print("Database Error:", error.orig)



        # User-friendly response

        print("User already exists")



        # -------------------------------------------------
        # WHY ROLLBACK IS IMPORTANT
        # -------------------------------------------------

        # In real SQLAlchemy projects:
        #
        # db.session.rollback()
        #
        # is mandatory after failed commit.
        #
        # Otherwise DB session becomes invalid.

        print("Database rollback executed")



# =====================================================
# STEP 4: MAIN PROGRAM
# =====================================================

print("\n==============================")
print("USER REGISTRATION SYSTEM")
print("==============================")



# Runtime input from user

email = input("\nEnter Email: ")



# Function call

register_user(email)



# =====================================================
# STEP 5: DISPLAY FINAL DATABASE
# =====================================================

print("\n==============================")
print("CURRENT DATABASE USERS")
print("==============================")

print(existing_emails)