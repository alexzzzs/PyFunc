#!/usr/bin/env python3
"""Comprehensive example showcasing all PyFunc features."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe, _

def main():
    print("🚀 PyFunc Comprehensive Example")
    print("=" * 50)
    
    # 1. Basic Pipeline Operations
    print("\n1. Basic Pipeline Operations")
    result = pipe([1, 2, 3, 4, 5]).filter(_ > 2).map(_ ** 2).to_list()
    print(f"   Numbers > 2, squared: {result}")
    
    # 2. String Processing
    print("\n2. String Processing")
    text = "  hello, beautiful world!  "
    result = (pipe(text)
              .apply(_.strip().title())
              .explode(" ")
              .filter(lambda w: len(w) > 5)
              .implode(" ")
              .surround("✨ ", " ✨")
              .get())
    print(f"   Processed text: {result}")
    
    # 3. Dictionary Operations
    print("\n3. Dictionary Operations")
    users = {
        "alice": {"age": 30, "city": "new york"},
        "bob": {"age": 25, "city": "san francisco"},
        "charlie": {"age": 35, "city": "chicago"}
    }
    
    result = (pipe(users)
              .with_items()
              .map(lambda item: (item[0].title(), item[1]))
              .map(lambda item: {
                  "name": item[0],
                  "age": item[1]["age"],
                  "city": item[1]["city"].title(),
                  "category": "young" if item[1]["age"] < 30 else "mature"
              })
              .to_list())
    
    print("   Processed users:")
    for user in result:
        print(f"     {user}")
    
    # 4. Function Composition
    print("\n4. Function Composition")
    # Create reusable transformations
    normalize_name = _.strip().title()
    double = _ * 2
    square = _ ** 2
    
    # Compose functions
    double_then_square = double >> square
    
    result = pipe(3).apply(double_then_square).get()
    print(f"   (3 * 2) ** 2 = {result}")
    
    # 5. Complex Data Processing Pipeline
    print("\n5. Complex Data Processing")
    
    # Sample e-commerce data
    orders = [
        {"id": 1, "customer": "  Alice Johnson  ", "items": ["laptop", "mouse"], "total": 1200.50},
        {"id": 2, "customer": "BOB SMITH", "items": ["keyboard"], "total": 75.00},
        {"id": 3, "customer": "charlie brown", "items": ["monitor", "cables", "stand"], "total": 450.25},
        {"id": 4, "customer": "Diana Prince", "items": ["tablet"], "total": 300.00},
        {"id": 5, "customer": "eve adams", "items": ["phone", "case", "charger"], "total": 800.75},
    ]
    
    # Process orders with complex pipeline
    processed_orders = (pipe(orders)
                       .debug("📦 Processing orders")
                       .map(lambda order: {
                           **order,
                           "customer": pipe(order["customer"]).apply(normalize_name).get(),
                           "item_count": len(order["items"]),
                           "avg_item_price": order["total"] / len(order["items"])
                       })
                       .filter(lambda order: order["total"] > 100)
                       .sort(key=lambda order: order["total"], reverse=True)
                       .take(3)
                       .to_list())
    
    print("   Top 3 high-value orders:")
    for order in processed_orders:
        print(f"     {order['customer']}: ${order['total']:.2f} ({order['item_count']} items)")
    
    # 6. Group By Operations
    print("\n6. Group By Operations")
    
    # Group orders by customer category
    categorized = (pipe(processed_orders)
                  .map(lambda order: {
                      **order,
                      "category": "premium" if order["total"] > 500 else "standard"
                  })
                  .group_by(_["category"])
                  .get())
    
    for category, orders in categorized.items():
        print(f"   {category.title()} customers: {len(orders)}")
        for order in orders:
            print(f"     - {order['customer']}: ${order['total']:.2f}")
    
    # 7. Template and Formatting
    print("\n7. Template and Formatting")
    
    template = "Dear {customer}, your order #{id} for ${total:.2f} is confirmed!"
    
    confirmations = (pipe(processed_orders)
                    .map(lambda order: pipe(template).template_fill(order).get())
                    .map(lambda msg: pipe(msg).surround("📧 ", "").get())
                    .to_list())
    
    print("   Order confirmations:")
    for confirmation in confirmations:
        print(f"     {confirmation}")
    
    # 8. Side Effects and Debugging
    print("\n8. Side Effects and Debugging")
    
    # Process with side effects
    audit_log = []
    
    result = (pipe([100, 200, 300, 400, 500])
              .do(lambda items: audit_log.append(f"Processing {len(items)} items"))
              .filter(_ > 250)
              .map(_ * 0.9)  # Apply 10% discount
              .do(lambda discounted: audit_log.append(f"After discount: {len(list(discounted))} items"))
              .to_list())
    
    print(f"   Final result: {result}")
    print("   Audit log:")
    for entry in audit_log:
        print(f"     - {entry}")
    
    # 9. Advanced Itertools Operations
    print("\n9. Advanced Operations")
    
    # Sliding window analysis
    sales_data = [100, 120, 90, 150, 200, 180, 220, 190]
    
    trends = (pipe(sales_data)
             .window(3, 1)  # 3-day moving window
             .map(lambda window: {
                 "period": f"Days {sales_data.index(window[0])+1}-{sales_data.index(window[0])+3}",
                 "avg": sum(window) / len(window),
                 "trend": "up" if window[-1] > window[0] else "down"
             })
             .to_list())
    
    print("   Sales trends (3-day moving average):")
    for trend in trends:
        print(f"     {trend['period']}: ${trend['avg']:.1f} ({trend['trend']})")
    
    print("\n🎉 All examples completed successfully!")

if __name__ == "__main__":
    main()