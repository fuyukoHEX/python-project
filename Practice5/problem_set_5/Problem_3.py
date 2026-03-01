import re

txt = input()
find_txt = input()

x = re.findall(find_txt, txt)

print(len(x))


