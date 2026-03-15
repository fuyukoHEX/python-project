n = int(input())
numbers = list(map(int, input().split()))

truthy_count = sum(map(bool, numbers))
print(truthy_count)