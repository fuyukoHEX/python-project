class StringHandler():
    def __init__(self, string):
        self.string = string
        self.getString()
    def getString(self):
        self.string = input()
        self.printString()
    def printString(self):
        s = self.string
        print(s.upper())


s = StringHandler("")