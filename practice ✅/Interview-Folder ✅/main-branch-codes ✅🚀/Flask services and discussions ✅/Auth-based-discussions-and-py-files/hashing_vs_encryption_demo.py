# =====================================================
# File Name: hashing_vs_encryption_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ Password Hashing
# ✅ Difference Between Hashing & Encryption
# ✅ One-Way Security Concept
# ✅ Backend Authentication Security
# ✅ Flask Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: IMPORT HASHING FUNCTION
# =====================================================

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



# =====================================================
# STEP 2: ORIGINAL PASSWORD
# =====================================================

# User enters password during signup

plain_password = "mysecret123"



# =====================================================
# STEP 3: HASH THE PASSWORD
# =====================================================

# Hashing converts password into
# irreversible secure format

hashed_password = generate_password_hash(
    plain_password
)



# =====================================================
# STEP 4: DISPLAY RESULTS
# =====================================================

print("\n==============================")
print("PASSWORD HASHING")
print("==============================")

print("Original Password:")
print(plain_password)

print("\nHashed Password:")
print(hashed_password)



# =====================================================
# STEP 5: LOGIN SIMULATION
# =====================================================

# User enters password during login

entered_password = input(
    "\nEnter Password For Login: "
)



# =====================================================
# STEP 6: PASSWORD VALIDATION
# =====================================================

# IMPORTANT:
#
# We DO NOT decrypt hashed password.
#
# Instead:
# check_password_hash()
# safely compares passwords.

is_valid = check_password_hash(
    hashed_password,
    entered_password
)



# =====================================================
# STEP 7: LOGIN RESULT
# =====================================================

print("\n==============================")
print("LOGIN RESULT")
print("==============================")

if is_valid:

    print("✅ Correct Password")

else:

    print("❌ Wrong Password")



# =====================================================
# STEP 8: HASHING VS ENCRYPTION
# =====================================================

print("\n==============================")
print("HASHING VS ENCRYPTION")
print("==============================")

print("""
HASHING:
---------
✅ One-way process
✅ Cannot be reversed
✅ Used for passwords
✅ More secure for authentication


ENCRYPTION:
------------
✅ Two-way process
✅ Can be decrypted
✅ Used for sensitive data transfer
✅ Requires secret key
""")



# =====================================================
# STEP 9: INTERVIEW NOTES
# =====================================================

# WHY hash passwords instead of encrypting?
#
# 1. Hashing is one-way
# 2. Passwords should never be reversible
# 3. Encryption can be decrypted
# 4. Hashing cannot
# 5. More secure for authentication systems
#
#
# IMPORTANT:
#
# Backend systems NEVER decrypt passwords.
#
# They only compare hashes using:
#
# check_password_hash()
#
# =====================================================

# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates difference between:
# 1. Hashing
# 2. Encryption
#
# HOW TO RUN:
# python hashing_vs_encryption_demo.py
#
# INPUT NEEDED:
# Login password runtime input.
#
# CORRECT INPUT:
# mysecret123
#
# WHAT THIS FILE TEACHES:
# ✅ Password hashing
# ✅ One-way security
# ✅ Authentication concepts
# ✅ Hash comparison
#
# IMPORTANT INTERVIEW POINT:
#
# HASHING:
# One-way process
#
# ENCRYPTION:
# Two-way reversible process
#
# Passwords should ALWAYS be hashed,
# NOT encrypted.
#
# REAL USE CASE:
# Authentication systems
#
# =====================================================