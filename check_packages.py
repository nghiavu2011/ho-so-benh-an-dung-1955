import sys
import subprocess

print("Python version:", sys.version)
for pkg in ["requests", "playwright", "selenium", "urllib3"]:
    try:
        __import__(pkg)
        print(f"Package '{pkg}' is installed.")
    except ImportError:
        print(f"Package '{pkg}' is NOT installed.")
