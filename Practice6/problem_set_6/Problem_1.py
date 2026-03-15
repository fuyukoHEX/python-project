n = int(input())
array = list(map(int, input().split()))

square = filter(lambda x: x % 2 == 0, array)

print(len(square))
