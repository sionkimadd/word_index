import unittest
from tests import *

def main():
    
    tests = [
        TestGoogleNewsFetcher,
        TestCSVtoSQL,
        TestSQLtoCSV,
        TestsortCSV,
        TestSentimentAnalysis,
        TestdatetimeColInserter,
        TestcompoundColInserter,
        TestSentimentPlotter
    ]
    
    suite = unittest.TestSuite(
        unittest.TestLoader().loadTestsFromTestCase(test) for test in tests
    )
    
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()