import subprocess

try:
    result = subprocess.run(['tesseract', '-v'], capture_output=True, text=True)
    print(result.stdout)
except FileNotFoundError:
    print("Tesseract is not installed or not found in PATH")
