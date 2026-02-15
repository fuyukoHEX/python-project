class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(self.balance)
        else:
            print("Insufficient Funds")


data = list(map(int, input().split()))

acc = Account(data[0])

for amount in data[1:]:
    acc.withdraw(amount)
