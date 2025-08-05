import sys
sys.path.insert(0, 'C:/Users/annab/AppData/Local/Programs/Python/Python313/Lib/site-packages')

try:
    import pyfunc.native_c as native_c
    print(dir(native_c))
except ImportError as e:
    print(f"Error importing native_c: {e}")

