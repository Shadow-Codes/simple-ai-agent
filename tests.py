from functions.run_python import run_python_file

result = run_python_file("calculator", "main.py")
print(f"{result}")

result = run_python_file("calculator", "tests.py")
print(f"{result}")

result = run_python_file("calculator", "../main.py")
print(f"{result}")

result = run_python_file("calculator", "nonexistent.py")
print(f"{result}")
