'''
🔴 Very Hard Level (3 Questions)
Q5: The E-Commerce System with Discounts (Hard)

Build a full e-commerce system with products, shopping carts, and discount strategies.

Requirements:

    Product Hierarchy:

        Product (base): id, name, price, category, stock

        Electronics: warranty_period

        Clothing: size, material

        Food: expiration_date, weight

    Discount System (Strategy Pattern):

        Interface DiscountStrategy with apply() method

        Implement: PercentageDiscount, FixedDiscount, BuyXGetYFree, CategoryDiscount

        Discounts can be combined

    Shopping Cart:

        Add/remove items

        Calculate total (with discounts)

        Apply coupon codes

        Validate stock

    Order System:

        Create orders from cart

        Track order status

        Generate invoices

    Inventory System:

        Track stock

        Alert when low

        Reserve items during checkout

    Use advanced OOP:

        Dataclasses for value objects

        Abstract classes for interfaces

        Property decorators for validation

        Magic methods for comparisons

Sample Output:
text

🛒 E-COMMERCE SYSTEM 🛒

📦 PRODUCTS:
1. Laptop (Electronics) - ₦450,000.00
   Warranty: 24 months
   Stock: 10

2. T-Shirt (Clothing) - ₦15,000.00
   Size: L, Material: Cotton
   Stock: 25

3. Chocolate (Food) - ₦1,500.00
   Weight: 200g, Expires: 2026-12-31
   Stock: 50

🛒 SHOPPING CART
Add products to cart...
Added: Laptop (2)
Added: T-Shirt (3)
Added: Chocolate (5)

Cart Total: ₦950,000.00

Available Discounts:
1. 10% off (SAVE10)
2. ₦5,000 off (SAVE5K)
3. Buy 2 Get 1 Free on T-Shirts (BOGO)

Apply discount: SAVE10
✅ Applied 10% off

New Total: ₦855,000.00

Apply additional discount? (y/n): y
Apply discount: BOGO
✅ Applied Buy 2 Get 1 Free on T-Shirts

New Total: ₦837,000.00

📋 CHECKOUT
1x Laptop @ ₦450,000.00 = ₦900,000.00
2x T-Shirt (free) @ ₦15,000.00 = ₦0.00
1x T-Shirt @ ₦15,000.00 = ₦15,000.00
5x Chocolate @ ₦1,500.00 = ₦7,500.00

Subtotal: ₦950,000.00
Discount: -₦113,000.00
Total: ₦837,000.00

Confirm order? (y/n): y
✅ Order placed! Order #ORD-001

📊 ORDER DETAILS
Order #ORD-001
Status: Confirmed
Total: ₦837,000.00

Items:
- Laptop (2)
- T-Shirt (3) [2 free]
- Chocolate (5)

Shipping to: Damilola, Lagos
Estimated delivery: 3-5 days

Concepts: Abstract classes, strategy pattern, dataclasses, property decorators, magic methods, complex logic
'''