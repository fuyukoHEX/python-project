n = int(input())
a = [2, 3, 5]
is_usual = False

for i in a:
    while n % i == 0:
        n /= i
    else:
        is_usual = True

if is_usual:
    print("Yes")
else:
    print("No")

