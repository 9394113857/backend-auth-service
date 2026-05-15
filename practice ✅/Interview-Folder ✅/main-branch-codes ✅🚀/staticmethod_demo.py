# =====================================================
# File Name: staticmethod_demo.py
# =====================================================

# =====================================================
# PURPOSE
# =====================================================
#
# This file demonstrates:
#
# ✅ @staticmethod
# ✅ Difference:
#       with staticmethod
#       without staticmethod
# ✅ Why services use static methods
# ✅ OOP interview concepts
# ✅ Backend architecture understanding
#
# =====================================================



# =====================================================
# EXAMPLE 1:
# NORMAL CLASS METHOD (WITHOUT STATICMETHOD)
# =====================================================

class NormalCalculator:



    # -------------------------------------------------
    # NORMAL INSTANCE METHOD
    # -------------------------------------------------
    #
    # Requires:
    # self
    #
    # Means:
    # object creation REQUIRED
    #
    # Example:
    #
    # calc = NormalCalculator()
    # calc.add_numbers()
    #
    # -------------------------------------------------

    def add_numbers(self, a, b):

        return a + b



# =====================================================
# USING NORMAL METHOD
# =====================================================

print("\n==============================")
print("WITHOUT STATICMETHOD")
print("==============================")



# Object creation REQUIRED

calc = NormalCalculator()



# Calling instance method

result1 = calc.add_numbers(10, 20)

print("Result:", result1)



# =====================================================
# EXAMPLE 2:
# STATIC METHOD
# =====================================================

class StaticCalculator:



    # -------------------------------------------------
    # STATIC METHOD
    # -------------------------------------------------
    #
    # No self required
    #
    # Object creation NOT required
    #
    # Can directly call using class name.
    #
    # -------------------------------------------------

    @staticmethod
    def add_numbers(a, b):

        return a + b



# =====================================================
# USING STATIC METHOD
# =====================================================

print("\n==============================")
print("WITH STATICMETHOD")
print("==============================")



# Direct class method call
# No object creation needed

result2 = StaticCalculator.add_numbers(10, 20)

print("Result:", result2)



# =====================================================
# REAL BACKEND SERVICE EXAMPLE
# =====================================================

class CartService:



    # -------------------------------------------------
    # WHY STATICMETHOD IN SERVICES?
    # -------------------------------------------------
    #
    # Service methods usually:
    #
    # ✅ don't store object state
    # ✅ don't need self
    # ✅ perform utility/business logic
    #
    # So:
    # object creation unnecessary
    #
    # -------------------------------------------------

    @staticmethod
    def add_to_cart(user_id, product_name):

        print("\n==============================")
        print("CART SERVICE")
        print("==============================")

        print(f"User ID: {user_id}")

        print(f"Product Added: {product_name}")



# =====================================================
# CALLING SERVICE METHOD
# =====================================================

# No object creation needed

CartService.add_to_cart(
    101,
    "iPhone 16"
)



# =====================================================
# WHY SERVICES COMMONLY USE STATICMETHOD?
# =====================================================

print("\n==============================")
print("WHY STATICMETHOD?")
print("==============================")

print("""
WITHOUT STATICMETHOD:
----------------------
❌ Object creation required
❌ More memory usage
❌ Unnecessary self usage


WITH STATICMETHOD:
-------------------
✅ Direct class access
✅ Cleaner service architecture
✅ Better utility methods
✅ No unnecessary objects
✅ Common in Flask services
""")



# =====================================================
# REAL FLASK SERVICE EXAMPLE
# =====================================================

# Example:
#
# class CheckoutService:
#
#     @staticmethod
#     def checkout(user_id, data):
#         pass
#
#
# WHY?
#
# checkout() only performs business logic.
#
# It does NOT need:
#
# self.name
# self.price
# self.anything
#
# So:
# @staticmethod is cleaner.
#
# =====================================================



# =====================================================
# QUICK REVISION NOTES
# =====================================================

# FILE PURPOSE:
# Demonstrates:
# 1. Normal methods
# 2. Static methods
# 3. Service architecture concepts
#
#
# HOW TO RUN:
#
# python staticmethod_demo.py
#
#
# INPUT NEEDED:
#
# No runtime input required.
#
#
# IMPORTANT INTERVIEW POINT:
#
# NORMAL METHOD:
#
# Requires:
# self
#
# Requires:
# object creation
#
#
# STATIC METHOD:
#
# No self
# No object creation
#
#
# WHY SERVICES USE STATICMETHOD?
#
# Because service methods:
#
# ✅ perform business logic
# ✅ don't need object state
# ✅ utility-like behavior
#
#
# REAL USE CASES:
#
# ✅ CartService
# ✅ CheckoutService
# ✅ OrderService
# ✅ AuthService
#
#
# REAL INTERVIEW ANSWER:
#
# @staticmethod used when:
#
# method does not depend on instance variables.
#
# Improves:
# ✅ clean architecture
# ✅ memory efficiency
# ✅ reusable service methods
#
# =====================================================