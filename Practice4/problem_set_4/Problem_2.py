def even_sequence(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

number = int(input())

first = True
for i in even_sequence(number):
    if not first:
        print(",", end="")
    print(i, end="")
    first = False