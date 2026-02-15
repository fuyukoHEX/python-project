class pair():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def sum(self, xa, xb):
        resa = self.a +xa
        resb = self.b + xb
        print(f"Result: {resa} {resb}")

data = list(map(int, input().split()))

obj = pair(data[0],data[1])
obj.sum(data[2],data[3])