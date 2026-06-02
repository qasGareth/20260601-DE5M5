import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from datacleaner import dataEnrich

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.xError_Transactions = pd.DataFrame()
        self.xTransactions = pd.DataFrame({
                                "Days allowed to borrow": ["2 weeks", "1 month", "3 days", "1 year", "1 week", "1 day", "2 weeks"],
                                "Book checkout": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01",
                                     "2024-01-01", "2024-01-01", "2024-03-01"]),
                                "Book Returned": pd.to_datetime(["2024-01-15", "2024-02-01", "2024-01-04", "2024-12-31",
                                     "2024-01-08", "2024-01-02", "2024-03-01"])})
        self.aTransactions = pd.DataFrame({
                                "Book checkout": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01",
                                     "2024-01-01", "2024-01-01", "2024-03-01"]),
                                "Book Returned": pd.to_datetime(["2024-01-15", "2024-02-01", "2024-01-04", "2024-12-31",
                                     "2024-01-08", "2024-01-02", "2024-03-01"]),
                                "Borrow Limit (Days)":    [14, 30, 3, 365, 7, 1, 14],
                                "Borrow Duration (Days)": [14, 31,  3, 365, 7, 1,  0]}) 
        self.tTransactions = dataEnrich(self.xTransactions)


    def test_dateenrich(self):
        assert_frame_equal(self.tTransactions, self.aTransactions)

if __name__ == "__main__":
    unittest.main()
