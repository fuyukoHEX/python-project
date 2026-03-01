import re

a = input()

words = re.findall(r'\b\w{3}\b', a)
print(len(words))