class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def get_sum(self):
        return self.num1 + self.num2
    
    def difference(self):
        return self.num1 - self.num2
    
    def product(self):
        return self.num1 * self.num2
    
    def quotient(self):
        return self.num1 / self.num2

if __name__ == "__main__":    
    myCalc = Calculator(144,12)
    print(f"{myCalc.num1} divided by {myCalc.num2} equals {myCalc.quotient()}")