n = int(input())
keys = input().split()
values = input().split()
query_key = input()

dictionary = dict(zip(keys, values))

if query_key in dictionary:
    print(dictionary[query_key])
else:
    print("Not found")