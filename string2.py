text = input("Enter text: ")
result = ""

for i in range(len(text)):
    char = text[i]
    char_code = ord(char)
    
    if char_code >= 65 and char_code <= 90:
        result += char

print(f"Result: {result}")