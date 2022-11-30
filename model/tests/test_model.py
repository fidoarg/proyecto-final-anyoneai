import unittest
import pandas as pd
import ml_service
import os


class TestMLService(unittest.TestCase):
    def test_predict(self):
        data = pd.read_csv('./tests/test_entry.csv').to_dict()
        class_name, pred_probability = ml_service.predict(data)
        self.assertEqual(class_name, 1)
        self.assertAlmostEqual(pred_probability, 0.4770884, 5)


if __name__ == "__main__":
    unittest.main()
