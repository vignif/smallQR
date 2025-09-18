import unittest
from utils.captcha import generate_captcha, validate_captcha
from utils.counter import get_counter, increment_counter
from pathlib import Path
import tempfile

class TestUtils(unittest.TestCase):
    def test_captcha_generation_and_validation(self):
        q, a = generate_captcha()
        self.assertIn("What is", q)
        self.assertTrue(validate_captcha(a, a))
        self.assertFalse(validate_captcha("wrong", a))

    def test_counter_file_operations(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "count.txt"
            # initial read -> 0
            self.assertEqual(get_counter(f), 0)
            self.assertEqual(increment_counter(f), 1)
            self.assertEqual(increment_counter(f), 2)
            self.assertEqual(get_counter(f), 2)

if __name__ == '__main__':
    unittest.main()
