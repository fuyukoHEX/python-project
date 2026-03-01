import re

a = input()
b = input()

pattern = re.escape(b)
matches = re.findall(pattern, a)

print(len(matches))