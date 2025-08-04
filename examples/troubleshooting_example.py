#!/usr/bin/env python3
"""Troubleshooting examples for common PyFunc issues."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

def main():
    print("🔧 PyFunc Troubleshooting Examples")
    print("=" * 50)
    
    # Sample data
    orders = [
        {"id": 1, "customer": "Alice", "total": 1200.50},
        {"id": 2, "customer": "Bob", "total": 450.25}
    ]
    
    # 1. F-String Template Issue
    print("\n1. ❌ Common Mistake: Using F-Strings with Template Mapping")
    print("   This will cause: TypeError: unsupported format string passed to Placeholder.__format__")
    print("   DON'T DO THIS:")
    print("   # result = pipe(orders).map(f\"Order #{_['id']} for {_['customer']}: ${_['total']:.2f}\")")
    
    print("\n   ✅ Correct Way: Use Regular String Templates")
    result = (pipe(orders)
              .map("Order #{id} for {customer}: ${total:.2f}")
              .to_list())
    
    print("   Result:")
    for line in result:
        print(f"     {line}")
    
    # 2. Dictionary Template with F-String Issue
    print("\n2. ❌ Another Common Mistake: F-Strings in Dictionary Templates")
    print("   This will also fail:")
    print("   # pipe(orders).map({\"formatted\": f\"Order #{_['id']}\"})  # DON'T DO THIS")
    
    print("\n   ✅ Correct Way: Use Lambda Functions for Complex Logic")
    result = (pipe(orders)
              .map({
                  "id": _["id"],
                  "customer": _["customer"],
                  "formatted": lambda x: f"Order #{x['id']} for {x['customer']}"  # Lambda is OK
              })
              .to_list())
    
    print("   Result:")
    for item in result:
        print(f"     {item}")
    
    # 3. Correct Template Mapping Examples
    print("\n3. ✅ Correct Template Mapping Patterns")
    
    # Simple string template
    print("\n   a) Simple String Template:")
    result = pipe(orders).map("Customer: {customer}, Total: ${total:.2f}").to_list()
    for line in result:
        print(f"      {line}")
    
    # Dictionary template with placeholders
    print("\n   b) Dictionary Template with Placeholders:")
    result = (pipe(orders)
              .map({
                  "order_id": _["id"],
                  "customer_name": _["customer"],
                  "discounted_total": _["total"] * 0.9
              })
              .to_list())
    for item in result:
        print(f"      {item}")
    
    # Dictionary template with lambda functions
    print("\n   c) Dictionary Template with Lambda Functions:")
    result = (pipe(orders)
              .map({
                  "id": _["id"],
                  "customer": _["customer"],
                  "category": lambda x: "Premium" if x["total"] > 1000 else "Standard",
                  "tax": lambda x: x["total"] * 0.08
              })
              .to_list())
    for item in result:
        print(f"      {item}")
    
    # 4. Chaining Templates
    print("\n4. ✅ Chaining Dictionary and String Templates")
    result = (pipe(orders)
              .map({
                  "id": _["id"],
                  "customer": _["customer"],
                  "discounted": _["total"] * 0.9
              })
              .map("Order #{id}: {customer} pays ${discounted:.2f}")
              .to_list())
    
    print("   Chained result:")
    for line in result:
        print(f"     {line}")
    
    print("\n🎯 Key Takeaways:")
    print("• Never use f-strings (f\"...\") with template mapping")
    print("• Use regular string templates: \"Hello {name}\"")
    print("• Use lambda functions for complex logic in dictionary templates")
    print("• Chain dictionary and string templates for powerful transformations")
    print("• Template mapping works with the data from the previous step in the pipeline")

if __name__ == "__main__":
    main()