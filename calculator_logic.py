class Calculate:

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add(self) -> float:
        return self.num1 + self.num2

    def subtract(self) -> float:
        return self.num1 - self.num2

    def multiply(self) -> float:
        return self.num1 * self.num2

    def divide(self) -> float:
        if self.num2 == 0:
            return "Error, Cant divide by 0"
        return self.num1 / self.num2

    def power(self) -> float:
        return self.num1**self.num2
