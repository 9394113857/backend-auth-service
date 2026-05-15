# =====================================================
# File Name: password_hashing_example.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ Password Hashing
# ✅ generate_password_hash()
# ✅ Backend Authentication Security
# ✅ Flask/Werkzeug Security
# ✅ Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: IMPORT HASHING FUNCTION
# =====================================================

# generate_password_hash()
#
# Converts plain password into secure hashed password

from werkzeug.security import generate_password_hash



# =====================================================
# STEP 2: GET PASSWORD INPUT
# =====================================================

# User enters password during registration/signup

password = input("Enter Password: ")



# =====================================================
# STEP 3: HASH THE PASSWORD
# =====================================================

# IMPORTANT:
#
# We NEVER store plain passwords in database.
#
# Instead:
# generate_password_hash()
# converts password into secure hash.

hashed_password = generate_password_hash(password)



# =====================================================
# STEP 4: DISPLAY RESULTS
# =====================================================

print("\n==============================")
print("PASSWORD HASHING RESULT")
print("==============================")



# Original password

print("\nOriginal Password:")
print(password)



# Hashed password

print("\nHashed Password:")
print(hashed_password)



# =====================================================
# STEP 5: INTERVIEW NOTES
# =====================================================

# WHY use generate_password_hash()?
#
# 1. Protects user passwords
# 2. Prevents plain password storage
# 3. Improves authentication security
# 4. Used during user registration
#
#
# REAL BACKEND FLOW:
#
# User Signup
#     ↓
# Password Entered
#     ↓
# generate_password_hash(password)
#     ↓
# Store hash in database
#
#
# IMPORTANT:
#
# Plain Password:
# mysecret123
#
# Stored Password:
# pbkdf2:sha256:.....
#
#
# BENEFITS:
#
# ✅ One-way hashing
# ✅ Cannot be reversed
# ✅ Secure authentication
#
# =====================================================

# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates password hashing.
#
# HOW TO RUN:
# python password_hashing_example.py
#
# INPUT NEEDED:
# Enter password at runtime.
#
# EXAMPLE INPUT:
# mysecret123
#
# WHAT THIS FILE TEACHES:
# ✅ generate_password_hash()
# ✅ Password security
# ✅ Signup authentication flow
#
# IMPORTANT INTERVIEW POINT:
#
# NEVER store plain passwords.
#
# Store:
# hashed_password
#
# instead of:
# actual password
#
# REAL USE CASE:
# User registration systems
#
# =====================================================