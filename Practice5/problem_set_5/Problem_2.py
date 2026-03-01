import re

txt = input()
sub_txt = input()
x = re.search(sub_txt, txt)

if x:
    print("Yes")
else:
    print("No")
