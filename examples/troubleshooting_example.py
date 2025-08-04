#!/usr/bin/env python3
"""Common mistakes and how to fix them in PyFunc template mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

def main():
    print("🔧 PyFunc Troubleshooting Guide")
    print("=" * 50)
    
    # Sample data for examples
    orders = [
        {"id": 1, "customer": "Alice", "total": 1200.50},
        {"id": 2, "customer": "Bob", "total": 450.25}
    ]
    
    print("\n1. ❌ Common Mistake: Using f-strings")
    print("   This will cause: TypeError: unsupported format string passed to Placeholder.__format__")
    print("   DON'T DO THIS:")
    print("   # result = pipe(orders).map(f\"Order #{_['id']} for {_['customer']}\")  # ❌ Error!")
    
    print("\n2. ✅ Correct Way: Use regular string templates")
    result = pipe(orders).map("Order #{id} for {customer}").to_list()
    print("   Code: pipe(orders).map(\"Order #{id} for {customer}\")")
    print("   Result:")
    for line in result:
        print(f"     {line}")
    
    print("\n3. ❌ Common Mistake: Wrong template variable names")
    print("   This will show empty or cause errors if keys don't match")
    # Example of what NOT to do:
    # result = pipe(orders).map("Hello {name}")  # ❌ 'name' doesn't exist
    
    print("\n4. ✅ Correct Way: Match your data structure")
    result = pipe(orders).map("Customer: {customer}, Total: ${total:.2f}").to_list()
    print("   Code: pipe(orders).map(\"Customer: {customer}, Total: ${total:.2f}\")")
    print("   Result:")
    for line in result:
        print(f"     {line}")
    
    print("\n5. ✅ Transform data first if needed")
    result = (pipe(orders)
              .map({"name": _["customer"], "amount": _["total"]})  # Transform keys
              .map("Hello {name}, you owe ${amount:.2f}")
              .to_list())
    print("   Code: Transform keys first, then use in template")
    print("   Result:")
    for line in result:
        print(f"     {line}")
    
    print("\n6. ✅ Dictionary templates with complex logic")
    result = (pipe(orders)
              .map({
                  "customer": _["customer"],
                  "total": _["total"],
                  "category": lambda x: "Premium" if x["total"] > 1000 else "Standard",
                  "discount": lambda x: x["total"] * 0.1 if x["total"] > 1000 else 0
              })
              .to_list())
    
    print("   Dictionary template with lambda functions:")
    for order in result:
        print(f"     {order}")
    
    print("\n7. ✅ Chaining dictionary and string templates")
    result = (pipe(orders)
              .map({
                  "customer": _["customer"],
                  "total": _["total"],
                  "discounted": _["total"] * 0.9
              })
              .map("{customer}: ${total:.2f} → ${discounted:.2f} (10% off)")
              .to_list())
    
    print("   Chained templates:")
    for line in result:
        print(f"     {line}")
    
    print("\n📝 Key Takeaways:")
    print("• Use regular strings, not f-strings for templates")
    print("• Template variable names must match dictionary keys")
    print("• Use placeholders (_[\"key\"]) in dictionary templates")
    print("• Use lambda functions for complex logic in dictionary templates")
    print("• Chain dictionary and string templates for powerful transformations")
    
    print("\n✅ Your original example (corrected):")
    ecommerce_orders = [
        {"id": 1, "customer": "Alice", "items": ["laptop", "mouse"], "total": 1200.50},
        {"id": 2, "customer": "Bob", "items": ["keyboard"], "total": 75.00},
        {"id": 3, "customer": "Charlie", "items": ["monitor", "stand"], "total": 450.25},
        {"id": 4, "customer": "Diana", "items": ["desk", "chair"], "total": 95.00}
    ]
    
    result = (pipe(ecommerce_orders)
              .filter(_["total"] > 100)
              .map({
                  "id": _["id"],
                  "customer": _["customer"],
                  "discounted_total": _["total"] * 0.9
              })
              .map("Order #{id} for {customer}: ${discounted_total:.2f}")  # ← No 'f' here!
              .to_list())
    
    print("   Final result:")
    for line in result:
        print(f"     {line}")

if __name__ == "__main__":
    main()