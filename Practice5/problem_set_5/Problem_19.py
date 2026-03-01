import re

a = input()

pattern = re.compile(r'\b\w+\b')
words = pattern.findall(a)

print(len(words))