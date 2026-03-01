import re

a = input()

words = re.findall(r'\w+', a)
print(len(words))