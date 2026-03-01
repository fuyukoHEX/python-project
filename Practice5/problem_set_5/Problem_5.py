import re

text = input()

if re.search(r'^[a-zA-Z].*\d$', text):
    print("Yes")
else:
    print("No")