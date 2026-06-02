import unittest
from calc import Calculator

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator(8,2)


    def test_sum(self):
        self.assertEqual(self.calculator.get_sum(), 10, "The answer was not 10")

    def test_difference(self):
        self.assertEqual(self.calculator.difference(), 6, "The answer was not 6")
    
    def test_product(self):
        self.assertEqual(self.calculator.product(), 16, "The answer was not 16")
    
    def test_quotient(self):
        self.assertEqual(self.calculator.quotient(), 4, "The answer was not 4")

if __name__ == "__main__":
    unittest.main()
