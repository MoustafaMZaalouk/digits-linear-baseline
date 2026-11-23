import unittest
import tempfile
import json
from pathlib import Path
from demo import run

class ExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)/'results.json'
        cls.r=run(cls.output)
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
    def test_output_matches_returned_result(self):
        self.assertEqual(json.loads(self.output.read_text()),self.r)
    def test_accuracy_beats_baseline(self):
        self.assertGreater(self.r['accuracy'],self.r['majority_accuracy'])
    def test_matrix_shape(self):
        self.assertEqual(len(self.r['confusion_matrix']),10)
    def test_counts(self):
        self.assertEqual(sum(map(sum,self.r['confusion_matrix'])),self.r['test_rows'])

if __name__ == "__main__":
    unittest.main()
