# ============================================================
# 🚀 Flask Microservice Internal Flow Simulation
# ============================================================
#
# PURPOSE:
# --------
# This program demonstrates COMPLETE INTERNAL FLOW of:
#
# Client JSON Request
#        ↓
# API Controller Layer
#        ↓
# JSON → Python dict conversion
#        ↓
# Service Layer
#        ↓
# Business Logic + DB Logic
#        ↓
# Python dict Response
#        ↓
# dict → JSON conversion
#        ↓
# Final HTTP JSON Response
#
# ============================================================
# INTERVIEW KEY CONCEPTS COVERED:
# ============================================================
#
# ✅ JSON
# ✅ Python dict
# ✅ request.get_json()
# ✅ jsonify()
# ✅ Controller Layer
# ✅ Service Layer
# ✅ Business Logic
# ✅ Status Codes
# ✅ Internal Data Conversion
# ✅ Input/Output Types
# ✅ API Flow
#
# ============================================================



# ============================================================
# 🟦 IMPORT JSON MODULE
# ============================================================
#
# json.loads()
# ----------------
# Converts:
# JSON String → Python dict
#
# json.dumps()
# ----------------
# Converts:
# Python dict → JSON String
#
# ============================================================

import json



# ============================================================
# 🟦 CLIENT SIDE
# ============================================================
#
# Imagine:
# --------
# Angular / React / Mobile App / Postman
#
# sending HTTP JSON request to backend.
#
# ============================================================

print("\n====================================================")
print("🟦 CLIENT SIDE")
print("====================================================\n")



# ============================================================
# Hardcoded RAW JSON request from client
# ============================================================
#
# IMPORTANT:
# -----------
# This is NOT Python dict yet.
#
# This is RAW JSON STRING.
#
# TYPE:
# -----
# str
#
# ============================================================

raw_json_request = '''
{
    "email": "raghu@gmail.com",
    "password": "123456",
    "role": "seller"
}
'''



# ============================================================
# PRINT RAW JSON REQUEST
# ============================================================

print("🚀 RAW JSON REQUEST RECEIVED FROM CLIENT:\n")

print(raw_json_request)



# ============================================================
# PRINT TYPE BEFORE CONVERSION
# ============================================================
#
# Expected Output:
# ----------------
# <class 'str'>
#
# WHY?
# ----
# Because JSON over HTTP initially comes as STRING.
#
# ============================================================

print("\n====================================================")
print("TYPE BEFORE CONVERSION")
print("====================================================")

print(type(raw_json_request))



# ============================================================
# 🟦 API CONTROLLER LAYER
# ============================================================
#
# REAL FLASK CODE:
# ----------------
#
# data = request.get_json()
#
# PURPOSE:
# --------
# Convert incoming JSON request
# → Python dict
#
# ============================================================

print("\n====================================================")
print("🟦 API CONTROLLER LAYER")
print("====================================================\n")



# ============================================================
# JSON STRING → PYTHON dict CONVERSION
# ============================================================
#
# json.loads()
# ------------
# Simulates:
#
# request.get_json()
#
# in Flask.
#
# ============================================================

data = json.loads(raw_json_request)



# ============================================================
# PRINT PYTHON dict AFTER CONVERSION
# ============================================================
#
# Expected Output:
# ----------------
#
# {
#    'email': 'raghu@gmail.com',
#    'password': '123456',
#    'role': 'seller'
# }
#
# ============================================================

print("🚀 AFTER JSON → PYTHON dict CONVERSION:\n")

print(data)



# ============================================================
# PRINT TYPE AFTER CONVERSION
# ============================================================
#
# Expected Output:
# ----------------
# <class 'dict'>
#
# WHY?
# ----
# Because Flask/json.loads converts JSON
# into Python dictionary object.
#
# ============================================================

print("\n====================================================")
print("TYPE AFTER CONVERSION")
print("====================================================")

print(type(data))



# ============================================================
# 🟦 EXTRACT VALUES FROM dict
# ============================================================
#
# Controller extracts required values.
#
# REAL FLASK CODE:
#
# email = data.get("email")
#
# ============================================================

print("\n====================================================")
print("🟦 EXTRACT VALUES FROM dict")
print("====================================================\n")



# ============================================================
# Extract email from dict
# ============================================================

email = data.get("email")



# ============================================================
# Extract password from dict
# ============================================================

password = data.get("password")



# ============================================================
# Extract role from dict
# ============================================================
#
# Default:
# --------
# "user"
#
# if role missing.
#
# ============================================================

role = data.get("role", "user")



# ============================================================
# PRINT EXTRACTED VALUES
# ============================================================

print("🚀 EXTRACTED VALUES:\n")

print("EMAIL:", email)
print("PASSWORD:", password)
print("ROLE:", role)



# ============================================================
# PRINT TYPES OF EXTRACTED VALUES
# ============================================================
#
# Expected Output:
# ----------------
# <class 'str'>
#
# WHY?
# ----
# Because dictionary values are strings.
#
# ============================================================

print("\n====================================================")
print("TYPES OF EXTRACTED VALUES")
print("====================================================")

print("email type:", type(email))
print("password type:", type(password))
print("role type:", type(role))



# ============================================================
# 🟦 SERVICE LAYER
# ============================================================
#
# PURPOSE:
# --------
# Handles:
#
# ✅ Business Logic
# ✅ Validation
# ✅ Database Operations
# ✅ Hashing
# ✅ JWT Logic
#
# ============================================================

print("\n====================================================")
print("🟦 SERVICE LAYER")
print("====================================================\n")



# ============================================================
# SERVICE FUNCTION
# ============================================================
#
# INPUT TYPES:
# -------------
# email    → str
# password → str
# role     → str
#
# OUTPUT:
# -------
# (dict, int)
#
# ============================================================

def register_user(email, password, role):


    # ========================================================
    # PRINT RECEIVED VALUES
    # ========================================================

    print("🚀 SERVICE RECEIVED VALUES:\n")

    print("email =", email)
    print("password =", password)
    print("role =", role)



    # ========================================================
    # PRINT INPUT TYPES
    # ========================================================

    print("\n================================================")
    print("SERVICE INPUT TYPES")
    print("================================================")

    print("email type:", type(email))
    print("password type:", type(password))
    print("role type:", type(role))



    # ========================================================
    # SIMULATED BUSINESS LOGIC
    # ========================================================
    #
    # Real projects may perform:
    #
    # ✅ Validation
    # ✅ Password Hashing
    # ✅ DB Save
    # ✅ JWT Creation
    # ✅ Email Sending
    #
    # ========================================================

    print("\n🚀 Performing business logic...")
    print("🚀 Hashing password...")
    print("🚀 Saving user into database...\n")



    # ========================================================
    # SERVICE RETURNS PYTHON dict
    # ========================================================
    #
    # IMPORTANT:
    # ----------
    # Service returns PYTHON dict.
    #
    # NOT JSON.
    #
    # ========================================================

    response_dict = {
        "message": "User registered successfully",
        "role": role
    }



    # ========================================================
    # HTTP STATUS CODE
    # ========================================================

    status_code = 201



    # ========================================================
    # PRINT RESPONSE dict
    # ========================================================

    print("🚀 SERVICE RETURN RESPONSE:\n")

    print(response_dict)



    # ========================================================
    # PRINT RESPONSE TYPE
    # ========================================================
    #
    # Expected:
    # ----------
    # <class 'dict'>
    #
    # ========================================================

    print("\n================================================")
    print("SERVICE RESPONSE TYPE")
    print("================================================")

    print(type(response_dict))



    # ========================================================
    # PRINT STATUS CODE
    # ========================================================

    print("\nSTATUS CODE:")
    print(status_code)



    # ========================================================
    # PRINT STATUS TYPE
    # ========================================================
    #
    # Expected:
    # ----------
    # <class 'int'>
    #
    # ========================================================

    print("\nSTATUS CODE TYPE:")
    print(type(status_code))



    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return response_dict, status_code



# ============================================================
# 🟦 CALL SERVICE FUNCTION
# ============================================================

response, status = register_user(email, password, role)



# ============================================================
# 🟦 CONTROLLER RECEIVES SERVICE RESPONSE
# ============================================================

print("\n====================================================")
print("🟦 CONTROLLER RECEIVES RESPONSE")
print("====================================================\n")



# ============================================================
# PRINT RESPONSE
# ============================================================

print("🚀 RESPONSE RECEIVED FROM SERVICE:\n")

print(response)



# ============================================================
# PRINT RESPONSE TYPE
# ============================================================

print("\n====================================================")
print("RESPONSE TYPE")
print("====================================================")

print(type(response))



# ============================================================
# PRINT STATUS
# ============================================================

print("\nSTATUS:")
print(status)



# ============================================================
# PRINT STATUS TYPE
# ============================================================

print("\nSTATUS TYPE:")
print(type(status))



# ============================================================
# 🟦 dict → JSON CONVERSION
# ============================================================
#
# REAL FLASK CODE:
#
# jsonify(response)
#
# PURPOSE:
# --------
# Convert Python dict
# → JSON response
#
# ============================================================

print("\n====================================================")
print("🟦 dict → JSON RESPONSE")
print("====================================================\n")



# ============================================================
# PYTHON dict → JSON STRING
# ============================================================
#
# json.dumps()
# ------------
# Simulates:
#
# jsonify()
#
# ============================================================

final_json_response = json.dumps(response, indent=4)



# ============================================================
# PRINT FINAL JSON RESPONSE
# ============================================================

print("🚀 FINAL JSON RESPONSE:\n")

print(final_json_response)



# ============================================================
# PRINT FINAL RESPONSE TYPE
# ============================================================
#
# Expected:
# ----------
# <class 'str'>
#
# WHY?
# ----
# Because JSON response is STRING format.
#
# ============================================================

print("\n====================================================")
print("FINAL RESPONSE TYPE")
print("====================================================")

print(type(final_json_response))



# ============================================================
# 🟦 COMPLETE FLOW SUMMARY
# ============================================================

print("\n====================================================")
print("🚀 COMPLETE FLOW SUMMARY")
print("====================================================\n")

print("1️⃣ Client sends RAW JSON string")
print("2️⃣ Controller converts JSON → Python dict")
print("3️⃣ Controller extracts string values")
print("4️⃣ Service receives Python strings")
print("5️⃣ Service performs business logic")
print("6️⃣ Service returns Python dict + status code")
print("7️⃣ Controller converts dict → JSON")
print("8️⃣ Final JSON response sent to client 🚀")



# ============================================================
# 🟦 EXPECTED FINAL OUTPUT FLOW
# ============================================================
#
# <class 'str'>
#         ↓
# <class 'dict'>
#         ↓
# <class 'str'>
#         ↓
# <class 'dict'>
#         ↓
# <class 'str'>
#
# ============================================================
#
# JSON String
#      ↓
# Python dict
#      ↓
# Extracted Python strings
#      ↓
# Service Layer
#      ↓
# Python dict response
#      ↓
# JSON String response
#
# ============================================================

print("\n====================================================")
print("🚀 FINAL TYPE CONVERSION FLOW")
print("====================================================\n")

print("JSON String")
print("     ↓")
print("Python dict")
print("     ↓")
print("Extracted Python strings")
print("     ↓")
print("Service Layer")
print("     ↓")
print("Python dict response")
print("     ↓")
print("JSON String response 🚀")

