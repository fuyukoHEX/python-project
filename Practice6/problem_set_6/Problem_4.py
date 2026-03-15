n = int(input())
array_1 = list(map(int, input().split()))
array_2 = list(map(int, input().split()))

dot_product = 0
for x, y in zip(array_1, array_2):
    dot_product += array_1 * array_2

print(dot_product)