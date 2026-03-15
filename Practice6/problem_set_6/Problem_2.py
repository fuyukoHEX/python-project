n = int(input())
array = list(map(int, input().split()))

even_number = map(lambda x: x % 2 == 0, array)

print(list(len(even_number)))
