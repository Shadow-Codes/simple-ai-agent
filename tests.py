from functions.get_file_content import get_file_content

result = get_file_content("calculator", "main.py")
print(f"{result}")

result = get_file_content("calculator", "pkg/calculator.py")
print(f"{result}")

result = get_file_content("calculator", "/bin/cat")
print(f"{result}")
