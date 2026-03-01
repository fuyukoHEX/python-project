import re

a = input()
b = input()
c = input()

pattern = re.escape(b)
result = re.sub(pattern, c, a)

print(result)