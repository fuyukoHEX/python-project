def generate_squares(n):
    for i in range(n + 1):
        yield i ** 2

def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

def div_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

def countdown(n):
    for i in range(n, -1, -1):
        yield i


print("Create a generator that generates the squares of numbers up to some number N.")
n = int(input())
for val in generate_squares(n):
    print(val)

print("Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.")
n = int(input())
print(",".join(even_numbers(n)))

print("Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.")
n = int(input())
for val in div_by_3_and_4(n):
    print(val)

print("Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a for loop and print each of the yielded values.")
a = int(input())
b = int(input())
for val in squares(a, b):
    print(val)

print("Implement a generator that returns all numbers from (n) down to 0.")
n = int(input())
for val in countdown(n):
    print(val)