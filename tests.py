import unittest
import pandas as pd
import numpy as np
import io
import sys
from app import StockPredictorApp

class TestStockPredictorApp(unittest.TestCase):
    def setUp(self):
        self.app = StockPredictorApp()

    def test_about(self):
        # Test if the about method shows the correct message
        with self.assertRaises(SystemExit) as cm:
            self.app.about()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_open_file(self):
        # Test if the file is correctly loaded
        data = {'Date': ['01/01/2021', '01/02/2021', '01/03/2021'],
                'Open': [1, 2, 3],
                'Close': [4, 5, 6]}
        file_like = io.StringIO()
        pd.DataFrame(data).to_csv(file_like, index=False)
        sys.stdin = file_like
        self.app.open_file()
        self.assertEqual(self.app.file_path, '')

    def test_predict(self):
        # Test if the prediction is correct
        data = {'Date': ['01/01/2021', '01/02/2021', '01/03/2021'],
                'Open': [1, 2, 3],
                'Close': [4, 5, 6]}
        file_like = io.StringIO()
        pd.DataFrame(data).to_csv(file_like, index=False)
        sys.stdin = file_like
        self.app.open_file()
        self.app.predict()
        self.assertEqual(self.app.result_text.get(), 'SVM: 8.201589819719819, Linear Regression: 10.0')
        
    def test_exit(self):
        # Test if the exit method terminates the program
        with self.assertRaises(SystemExit) as cm:
            self.app.exit()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, None)

if __name__ == '__main__':
    unittest.main()