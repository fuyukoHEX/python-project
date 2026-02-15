n = int(input())
array = list(map(int, input().split()))
q = int(input())

for _ in range(q):
    command = input().split()
    op = command[0]
    
    if op == "add":
        val = int(command[1])
        array = [x + val for x in array]
        
    elif op == "multiply":
        val = int(command[1])
        array = [x * val for x in array]
        
    elif op == "power":
        val = int(command[1])
        array = [x ** val for x in array]
        
    elif op == "abs":
        array = [abs(x) for x in array]

print(*array)