import re

a = input()

if re.search(r'cat|dog', a):
    print("Yes")
else:
    print("No")