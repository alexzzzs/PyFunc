import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyfunc import pipe

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
operand = 3
bits = 2

# --- Python Backend ---
print("\n--- Python Bitwise Operations ---")
print(f"AND {operand}: {pipe(data).bitwise_and(operand).to_list()}")
print(f"OR {operand}: {pipe(data).bitwise_or(operand).to_list()}")
print(f"XOR {operand}: {pipe(data).bitwise_xor(operand).to_list()}")
print(f"NOT: {pipe(data).bitwise_not().to_list()}")
print(f"Left Shift {bits}: {pipe(data).left_shift(bits).to_list()}")
print(f"Right Shift {bits}: {pipe(data).right_shift(bits).to_list()}")

# --- C Backend ---
print("\n--- C Bitwise Operations ---")
print(f"AND {operand}: {pipe(data).bitwise_and(operand).to_list()}")
print(f"OR {operand}: {pipe(data).bitwise_or(operand).to_list()}")
print(f"XOR {operand}: {pipe(data).bitwise_xor(operand).to_list()}")
print(f"NOT: {pipe(data).bitwise_not().to_list()}")
print(f"Left Shift {bits}: {pipe(data).left_shift(bits).to_list()}")
print(f"Right Shift {bits}: {pipe(data).right_shift(bits).to_list()}")
