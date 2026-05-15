# =====================================================
# File Name: set_password_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ set_password() method
# ✅ Password Hashing
# ✅ Encapsulation
# ✅ Reusable Security Logic
# ✅ Backend Authentication Concepts
# ✅ Flask Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: IMPORT PASSWORD HASH FUNCTION
# =====================================================

from werkzeug.security import generate_password_hash



# =====================================================
# STEP 2: CREATE USER CLASS
# =====================================================

class User:



    # -------------------------------------------------
    # CONSTRUCTOR
    # -------------------------------------------------

    def __init__(self, email):

        self.email = email

        # Initially password hash is empty
        self.password_hash = None



    # =================================================
    # set_password METHOD
    # =================================================

    def set_password(self, password):


        # ---------------------------------------------
        # WHY THIS METHOD?
        # ---------------------------------------------
        #
        # Instead of hashing password everywhere:
        #
        # generate_password_hash(password)
        #
        # we centralize security logic in one place.
        #
        # Benefits:
        # ✅ reusable
        # ✅ cleaner code
        # ✅ centralized security handling
        #
        # ---------------------------------------------



        # Convert plain password into hashed password

        self.password_hash = generate_password_hash(
            password
        )



# =====================================================
# STEP 3: CREATE USER OBJECT
# =====================================================

user1 = User("raghu@gmail.com")



# =====================================================
# STEP 4: SET PASSWORD
# =====================================================

# Calling reusable password hashing method

user1.set_password("mysecret123")



# =====================================================
# STEP 5: DISPLAY RESULTS
# =====================================================

print("\n==============================")
print("USER DETAILS")
print("==============================")

print("Email:", user1.email)

print("\nStored Password Hash:")
print(user1.password_hash)



# =====================================================
# STEP 6: INTERVIEW NOTES
# =====================================================

# WHY create set_password() method?
#
# 1. Encapsulates password hashing logic
# 2. Improves code reusability
# 3. Keeps code clean
# 4. Centralizes security handling
# 5. Avoids repeated hashing code
#
#
# BAD PRACTICE:
#
# user.password_hash =
# generate_password_hash(password)
#
# repeated everywhere
#
#
# GOOD PRACTICE:
#
# user.set_password(password)
#
# centralized reusable logic
#
# =====================================================

# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates set_password() method.
#
# HOW TO RUN:
# python set_password_demo.py
#
# INPUT NEEDED:
# No runtime input required.
#
# WHAT THIS FILE TEACHES:
# ✅ Encapsulation
# ✅ Reusable security logic
# ✅ Password hashing methods
# ✅ OOP concepts
#
# IMPORTANT INTERVIEW POINT:
#
# GOOD PRACTICE:
# user.set_password(password)
#
# BAD PRACTICE:
# generate_password_hash()
# repeated everywhere
#
# REAL USE CASE:
# Flask User model methods
#
# =====================================================