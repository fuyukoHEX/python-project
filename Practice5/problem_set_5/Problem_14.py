import re

a = input()

pattern = re.compile(r'^\d+$')

if pattern.fullmatch(a):
    print("Match")
else:
    print("No match")