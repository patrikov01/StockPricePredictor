"""
Unit tests for StockPredictorApp class
"""
import unittest
import io
import sys
import pandas as pd
from app import StockPredictorApp

class TestStockPredictorApp(unittest.TestCase):
    """
    Class to test the StockPredictorApp class.
    """
    def setUp(self):
        self.app = StockPredictorApp()

    def test_about(self):
        """
        Test if the about method shows the correct message
        """
        with self.assertRaises(SystemExit) as exit_cm:
            self.app.about()
        the_exception = exit_cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_open_file(self):
        """
        Test if the file is correctly loaded
        """
        data = {'Date': [...],
                'Open': [...],
                'Close': [...]}
        file_like = io.StringIO()
        pd.DataFrame(data).to_csv(file_like, index=False)
        sys.stdin = file_like
        self.app.open_file()
        self.assertEqual(self.app.file_path, '')

    def test_predict(self):
        """ 
        Test if the prediction is correct
        """
        data = {'Date': [...],
                'Open': [...],
                'Close': [...]}
        file_like = io.StringIO()
        pd.DataFrame(data).to_csv(file_like, index=False)
        sys.stdin = file_like
        self.app.open_file()
        self.app.predict()
        self.assertEqual(self.app.result_text.get(), 'SVM: ..., Linear Regression: ...')

    def test_exit(self):
        """
        Test if the exit method terminates the program
        """
        with self.assertRaises(SystemExit) as exit_cm:
            self.app.exit()
        the_exception = exit_cm.exception
        self.assertEqual(the_exception.code, None)

if __name__ == '__main__':
    unittest.main()
