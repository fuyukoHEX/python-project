m = int(input())

g = 0
n = 0

for _ in range(m):
    command, value_str = input().split()
    value = int(value_str)
    if command == "global":
        g += value
    elif command == "nonlocal":
        n += value
print(f"{g} {n}")