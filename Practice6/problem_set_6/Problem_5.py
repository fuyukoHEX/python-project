s = input().lower()
vowels = "aeiou"

if any(char in vowels for char in s):
    print("Yes")
else:
    print("No")