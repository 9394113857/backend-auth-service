# =====================================================
# File Name: jwt_blocklist_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ JWT Blocklist Concept
# ✅ Logout Token Invalidation
# ✅ Stateless Authentication
# ✅ Token Revocation
# ✅ Backend Security Concepts
# ✅ Flask Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: HARDCODED ACTIVE JWT TOKEN
# =====================================================

# Imagine this token is generated after login

active_token = "jwt_token_12345"



# =====================================================
# STEP 2: TOKEN BLOCKLIST DATABASE SIMULATION
# =====================================================

# In real Flask projects:
#
# TokenBlocklist(db.Model)
#
# stores blacklisted JWT token IDs (jti)

token_blocklist = []



# =====================================================
# STEP 3: ACCESS PROTECTED API
# =====================================================

def access_protected_route(token):


    print("\n==============================")
    print("CHECKING TOKEN ACCESS")
    print("==============================")



    # -------------------------------------------------
    # CHECK TOKEN BLOCKLIST
    # -------------------------------------------------

    # If token exists in blocklist:
    # deny access

    if token in token_blocklist:

        print("❌ Access Denied")
        print("Token is blacklisted")



    else:

        print("✅ Access Granted")
        print("Valid JWT Token")



# =====================================================
# STEP 4: USER LOGIN
# =====================================================

print("\n==============================")
print("USER LOGIN")
print("==============================")

print("JWT Token Generated:")
print(active_token)



# =====================================================
# STEP 5: ACCESS BEFORE LOGOUT
# =====================================================

# Token works successfully

access_protected_route(active_token)



# =====================================================
# STEP 6: USER LOGOUT
# =====================================================

print("\n==============================")
print("USER LOGOUT")
print("==============================")



# -----------------------------------------------------
# WHY BLOCKLIST IMPORTANT?
# -----------------------------------------------------
#
# JWT is stateless.
#
# Even after logout:
#
# token remains valid until expiry.
#
# So we store token inside blocklist
# to invalidate it before expiration.
#
# -----------------------------------------------------



# Add token into blacklist

token_blocklist.append(active_token)

print("Token added to blocklist")



# =====================================================
# STEP 7: ACCESS AFTER LOGOUT
# =====================================================

# Same token now becomes invalid

access_protected_route(active_token)



# =====================================================
# STEP 8: DISPLAY BLOCKLIST
# =====================================================

print("\n==============================")
print("TOKEN BLOCKLIST")
print("==============================")

print(token_blocklist)



# =====================================================
# STEP 9: INTERVIEW NOTES
# =====================================================

# WHY store tokens in blocklist?
#
# 1. JWT is stateless
# 2. Logout does NOT automatically destroy token
# 3. Token remains valid until expiry
# 4. Blocklist invalidates token early
# 5. Improves authentication security
#
#
# REAL FLASK JWT FLOW:
#
# 1. User Login
#    -> JWT generated
#
# 2. User Logout
#    -> jti stored in TokenBlocklist table
#
# 3. Every protected request:
#    -> backend checks blocklist
#
# 4. If token exists:
#    -> access denied
#
# =====================================================


# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates JWT blocklist/logout flow.
#
# HOW TO RUN:
# python jwt_blocklist_demo.py
#
# INPUT NEEDED:
# No runtime input required.
#
# WHAT THIS FILE TEACHES:
# ✅ JWT authentication
# ✅ Token blocklisting
# ✅ Logout invalidation
# ✅ Stateless authentication
#
# IMPORTANT INTERVIEW POINT:
#
# JWT remains valid after logout
# until token expiry.
#
# Blocklist invalidates token early.
#
# REAL USE CASE:
# Logout APIs
# JWT authentication systems
#
# =====================================================