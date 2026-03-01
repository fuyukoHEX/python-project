import re

a = input()

uppercase_letters = re.findall(r'[A-Z]', a)
print(len(uppercase_letters))