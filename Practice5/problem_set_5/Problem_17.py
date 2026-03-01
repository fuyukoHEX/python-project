import re

a = input()

dates = re.findall(r'\d{2}/\d{2}/\d{4}', a)
print(len(dates))