import re

a = input()

numbers = re.findall(r'\d{2,}', a)
print(" ".join(numbers))