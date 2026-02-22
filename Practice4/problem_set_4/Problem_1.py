def square(n):
    for i in range(n):
        yield i * i

number = int(input())

for i in square(number):
    print(number)