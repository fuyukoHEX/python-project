def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

n = int(input())

isFirst = True
for i in fibonacci(n):
    if not isFirst:
        print(",", end="")
    print(i, end="")
    isFirst = False
    