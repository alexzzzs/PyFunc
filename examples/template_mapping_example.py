#!/usr/bin/env python3
"""Template mapping examples showcasing dictionary and string templates."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

def main():
    print("🎯 PyFunc Template Mapping Examples")
    print("=" * 50)
    
    # 1. Dictionary Template Mapping
    print("\n1. Dictionary Template Mapping")
    
    employees = [
        {"name": "Alice Johnson", "age": 30, "salary": 75000, "department": "Engineering"},
        {"name": "Bob Smith", "age": 25, "salary": 55000, "department": "Marketing"},
        {"name": "Charlie Brown", "age": 35, "salary": 85000, "department": "Engineering"},
        {"name": "Diana Prince", "age": 28, "salary": 65000, "department": "Sales"}
    ]
    
    # Transform employee data using dictionary templates
    transformed = pipe(employees).map({
        "full_name": _["name"],
        "age_category": lambda x: "senior" if x["age"] > 30 else "junior",
        "annual_bonus": _["salary"] * 0.15,
        "dept": _["department"],
        "total_compensation": lambda x: x["salary"] + (x["salary"] * 0.15)
    }).to_list()
    
    print("   Transformed employee data:")
    for emp in transformed:
        print(f"     {emp['full_name']}: {emp['age_category']}, bonus: ${emp['annual_bonus']:,.2f}")
    
    # 2. String Template Mapping
    print("\n2. String Template Mapping")
    
    products = [
        {"name": "Laptop", "price": 1299.99, "stock": 15, "category": "Electronics"},
        {"name": "Coffee Mug", "price": 12.50, "stock": 100, "category": "Kitchen"},
        {"name": "Wireless Mouse", "price": 29.99, "stock": 50, "category": "Electronics"}
    ]
    
    # Create product descriptions using string templates
    descriptions = pipe(products).map(
        "{name} ({category}): ${price:.2f} - {stock} units in stock"
    ).to_list()
    
    print("   Product descriptions:")
    for desc in descriptions:
        print(f"     {desc}")
    
    # 3. E-commerce Order Processing (Your Original Example)
    print("\n3. E-commerce Order Processing")
    
    ecommerce_orders = [
        {"id": 1, "customer": "Alice", "items": ["laptop", "mouse"], "total": 1200.50},
        {"id": 2, "customer": "Bob", "items": ["keyboard"], "total": 75.00},
        {"id": 3, "customer": "Charlie", "items": ["monitor", "stand"], "total": 450.25},
        {"id": 4, "customer": "Diana", "items": ["desk", "chair"], "total": 95.00}
    ]
    
    # Process orders with filtering, transformation, and formatting
    result = (pipe(ecommerce_orders)
              .filter(_["total"] > 100)  # Filter orders with total > $100
              .map({
                  "id": _["id"],
                  "customer": _["customer"],
                  "discounted_total": _["total"] * 0.9  # Apply a 10% discount
              })
              .map("Order #{id} for {customer}: ${discounted_total:.2f}")
              .to_list())
    
    print("   Processed orders:")
    for order in result:
        print(f"     {order}")
    
    # 4. Complex Data Analysis Pipeline
    print("\n4. Complex Data Analysis Pipeline")
    
    sales_data = [
        {"region": "North", "month": "Jan", "sales": 45000, "target": 50000},
        {"region": "South", "month": "Jan", "sales": 52000, "target": 48000},
        {"region": "East", "month": "Jan", "sales": 38000, "target": 40000},
        {"region": "West", "month": "Jan", "sales": 61000, "target": 55000},
        {"region": "North", "month": "Feb", "sales": 48000, "target": 50000},
        {"region": "South", "month": "Feb", "sales": 55000, "target": 48000}
    ]
    
    # Analyze sales performance
    analysis = (pipe(sales_data)
                .map({
                    "region": _["region"],
                    "month": _["month"],
                    "performance": _["sales"] / _["target"],
                    "variance": _["sales"] - _["target"],
                    "status": lambda x: "✅ Above Target" if x["sales"] > x["target"] else "❌ Below Target"
                })
                .filter(_["performance"] > 1.0)  # Only above-target regions
                .map("Region {region} ({month}): {performance:.1%} of target {status}")
                .to_list())
    
    print("   Sales analysis (above-target regions only):")
    for result in analysis:
        print(f"     {result}")
    
    # 5. User Profile Generation
    print("\n5. User Profile Generation")
    
    users = [
        {"username": "alice_dev", "email": "alice@example.com", "join_date": "2023-01-15", "posts": 45},
        {"username": "bob_designer", "email": "bob@example.com", "join_date": "2023-03-22", "posts": 23},
        {"username": "charlie_pm", "email": "charlie@example.com", "join_date": "2022-11-08", "posts": 67}
    ]
    
    # Generate user profiles
    profiles = (pipe(users)
                .map({
                    "display_name": lambda x: x["username"].replace("_", " ").title(),
                    "email": _["email"],
                    "activity_level": lambda x: "High" if x["posts"] > 50 else "Medium" if x["posts"] > 20 else "Low",
                    "posts_count": _["posts"]
                })
                .map("👤 {display_name} ({email}) - {activity_level} activity ({posts_count} posts)")
                .to_list())
    
    print("   User profiles:")
    for profile in profiles:
        print(f"     {profile}")
    
    print("\n🎉 Template mapping examples completed!")
    print("\nKey Features Demonstrated:")
    print("• Dictionary templates with placeholders and lambda functions")
    print("• String templates with formatting specifiers")
    print("• Complex data transformations and filtering")
    print("• Real-world data processing scenarios")

if __name__ == "__main__":
    main()