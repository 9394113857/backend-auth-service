# =====================================================
# File Name: check_password_hash_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ Password Hashing
# ✅ check_password_hash()
# ✅ Login Authentication Logic
# ✅ Flask/Werkzeug Security Concepts
# ✅ Backend Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: IMPORT REQUIRED FUNCTIONS
# =====================================================

# generate_password_hash
# Converts plain password into hashed password

# check_password_hash
# Compares entered password with stored hash

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



# =====================================================
# STEP 2: USER REGISTRATION SIMULATION
# =====================================================

# Imagine user enters password during signup

original_password = "mysecret123"



# Convert plain password into secure hash

stored_password_hash = generate_password_hash(
    original_password
)



# =====================================================
# STEP 3: DISPLAY HASHED PASSWORD
# =====================================================

print("\n==============================")
print("HASHED PASSWORD")
print("==============================")

print(stored_password_hash)



# =====================================================
# STEP 4: LOGIN SIMULATION
# =====================================================

# User enters password during login

entered_password = input(
    "\nEnter Password For Login: "
)



# =====================================================
# STEP 5: PASSWORD VALIDATION
# =====================================================

# check_password_hash compares:
#
# 1. Stored hashed password
# 2. User entered password
#
# Returns:
# True  -> Correct password
# False -> Wrong password

is_valid_user = check_password_hash(
    stored_password_hash,
    entered_password
)



# =====================================================
# STEP 6: LOGIN RESULT
# =====================================================

print("\n==============================")
print("LOGIN RESULT")
print("==============================")

if is_valid_user:

    print("✅ Login Successful")

else:

    print("❌ Invalid Password")



# =====================================================
# STEP 7: INTERVIEW NOTES
# =====================================================

# WHY check_password_hash() IMPORTANT?
#
# 1. Safely compares passwords
# 2. Prevents plain password storage
# 3. Used during login authentication
# 4. Improves backend security
#
# Real Production Usage:
#
# if check_password_hash(user.password_hash, password):
#     login_user(user)
#
# =====================================================

# Paste these comment blocks at END of each file for fast revision before interviews 🚀

# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates login password verification.
#
# HOW TO RUN:
# python check_password_hash_demo.py
#
# INPUT NEEDED:
# Enter login password at runtime.
#
# CORRECT INPUT:
# mysecret123
#
# WRONG INPUT:
# anything_else
#
# WHAT THIS FILE TEACHES:
# ✅ check_password_hash()
# ✅ Login authentication
# ✅ Password validation
# ✅ Hash comparison
#
# IMPORTANT INTERVIEW POINT:
# Backend NEVER decrypts passwords.
#
# Instead:
# check_password_hash()
# safely compares passwords.
#
# REAL USE CASE:
# User login systems
#
# =====================================================