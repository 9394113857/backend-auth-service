# =====================================================
# File Name: jwt_required_and_identity_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ @jwt_required()
# ✅ get_jwt_identity()
# ✅ JWT Authentication Flow
# ✅ Protected Routes
# ✅ User Identity Extraction
# ✅ Backend Security Concepts
# ✅ Flask Interview Practice
#
# =====================================================



# =====================================================
# STEP 1: SIMULATED JWT TOKEN DATABASE
# =====================================================

# Imagine these are valid logged-in users

valid_tokens = {
    "token_abc123": 101,
    "token_xyz999": 202
}



# =====================================================
# STEP 2: jwt_required() SIMULATION
# =====================================================

# In real Flask:
#
# @jwt_required()
#
# checks:
# ✅ token exists
# ✅ token valid
# ✅ token not expired
# ✅ token not blacklisted
#
# BEFORE route executes.

def jwt_required(token):


    print("\n==============================")
    print("JWT AUTHENTICATION CHECK")
    print("==============================")



    # -------------------------------------------------
    # CHECK TOKEN EXISTS
    # -------------------------------------------------

    if not token:

        print("❌ No JWT Token Provided")
        return False



    # -------------------------------------------------
    # CHECK TOKEN VALIDITY
    # -------------------------------------------------

    if token not in valid_tokens:

        print("❌ Invalid JWT Token")
        return False



    # -------------------------------------------------
    # TOKEN SUCCESS
    # -------------------------------------------------

    print("✅ Valid JWT Token")
    return True



# =====================================================
# STEP 3: get_jwt_identity() SIMULATION
# =====================================================

# In real Flask:
#
# get_jwt_identity()
#
# extracts authenticated user identity
# from JWT token.

def get_jwt_identity(token):


    print("\n==============================")
    print("EXTRACTING USER IDENTITY")
    print("==============================")



    # -------------------------------------------------
    # EXTRACT USER ID
    # -------------------------------------------------

    user_id = valid_tokens[token]



    print(f"✅ Authenticated User ID: {user_id}")

    return user_id



# =====================================================
# STEP 4: PROTECTED ROUTE SIMULATION
# =====================================================

# Simulating:
#
# @jwt_required()
# def add_to_cart():
#
# protected backend API

def add_to_cart(token):


    print("\n==============================")
    print("ADD TO CART API")
    print("==============================")



    # -------------------------------------------------
    # STEP 1:
    # JWT AUTH CHECK
    # -------------------------------------------------

    is_authenticated = jwt_required(token)



    # If token invalid:
    # stop route execution

    if not is_authenticated:

        print("Access Denied")
        return



    # -------------------------------------------------
    # STEP 2:
    # EXTRACT USER IDENTITY
    # -------------------------------------------------

    user_id = get_jwt_identity(token)



    # -------------------------------------------------
    # STEP 3:
    # BUSINESS LOGIC
    # -------------------------------------------------

    print("\nAdding products into cart...")



    # -------------------------------------------------
    # WHY USER ID IMPORTANT?
    # -------------------------------------------------

    # Cart must belong to logged-in user.
    #
    # Example:
    #
    # User 101 -> own cart
    # User 202 -> own cart

    print(f"Cart updated for User ID: {user_id}")



# =====================================================
# STEP 5: TEST CASES
# =====================================================

print("\n==============================")
print("TEST CASE 1 - VALID TOKEN")
print("==============================")

add_to_cart("token_abc123")



print("\n\n==============================")
print("TEST CASE 2 - INVALID TOKEN")
print("==============================")

add_to_cart("wrong_token")



# =====================================================
# STEP 6: INTERVIEW NOTES
# =====================================================

# BEFORE ROUTE EXECUTION:
#
# @jwt_required()
# checks:
#
# 1. Token exists
# 2. Token valid
# 3. Token not expired
# 4. Token not blacklisted
#
#
# AFTER AUTH SUCCESS:
#
# get_jwt_identity()
# extracts:
#
# ✅ authenticated user ID
#
#
# WHY IMPORTANT?
#
# Backend should NOT trust:
#
# frontend user_id
#
# Instead:
# JWT identity used securely.
#
#
# REAL PRODUCTION FLOW:
#
# Frontend Login
#      ↓
# JWT Token Generated
#      ↓
# Frontend sends token
#      ↓
# @jwt_required() validates token
#      ↓
# get_jwt_identity() extracts user
#      ↓
# Protected API executes
#
# =====================================================

# =====================================================
# QUICK REVISION NOTES
# =====================================================
#
# FILE PURPOSE:
# Demonstrates complete JWT protected API flow.
#
# Covers:
# ✅ @jwt_required()
# ✅ get_jwt_identity()
# ✅ Protected routes
# ✅ JWT authentication
# ✅ User identity extraction
#
#
# HOW TO RUN:
#
# python jwt_required_and_identity_demo.py
#
#
# INPUT NEEDED:
#
# No runtime input required.
#
#
# WHAT THIS FILE SIMULATES:
#
# Frontend Login
#       ↓
# JWT Token Generated
#       ↓
# Frontend sends token
#       ↓
# Backend validates token
#       ↓
# User identity extracted
#       ↓
# Protected API executes
#
#
# IMPORTANT UNDERSTANDING:
#
# BEFORE ROUTE EXECUTION:
#
# @jwt_required()
#
# checks:
#
# 1. Token exists
# 2. Token valid
# 3. Token not expired
# 4. Token not blacklisted
#
#
# AFTER TOKEN SUCCESS:
#
# get_jwt_identity()
#
# extracts:
#
# ✅ authenticated user ID
#
#
# WHY IMPORTANT?
#
# Backend should NEVER trust:
#
# ❌ user_id from frontend
#
# Instead:
#
# ✅ JWT identity used securely
#
#
# TEST CASE 1:
#
# add_to_cart("token_abc123")
#
# OUTPUT:
# ✅ Valid token
# ✅ User authenticated
# ✅ Cart updated
#
#
# TEST CASE 2:
#
# add_to_cart("wrong_token")
#
# OUTPUT:
# ❌ Invalid token
# ❌ Access denied
#
#
# REAL PRODUCTION USE CASES:
#
# ✅ Cart APIs
# ✅ Checkout APIs
# ✅ Orders APIs
# ✅ Profile APIs
# ✅ Seller APIs
#
#
# IMPORTANT INTERVIEW POINT:
#
# @jwt_required()
#
# works BEFORE route execution.
#
#
# get_jwt_identity()
#
# works AFTER successful authentication.
#
#
# REAL FLASK EXAMPLE:
#
# @jwt_required()
# def get_orders():
#
#     user_id = get_jwt_identity()
#
#     return OrderService.get_orders(user_id)
#
#
# =====================================================

