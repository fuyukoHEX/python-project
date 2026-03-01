import re

a = input()
b = input()

parts = re.split(b, a)
print(",".join(parts))