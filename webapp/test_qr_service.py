import unittest
from services.qr_service import generate_qr_min_version, generate_qr_manual, decode_qr

class TestQRService(unittest.TestCase):
    def test_generate_min_version_basic(self):
        png_bytes, version = generate_qr_min_version("hello")
        self.assertIsInstance(png_bytes, bytes)
        self.assertGreater(version, 0)
        self.assertLessEqual(version, 40)

    def test_generate_manual_version(self):
        png_bytes = generate_qr_manual("data", 5, "L")
        self.assertTrue(png_bytes.startswith(b"\x89PNG"), "Should produce PNG bytes")

    def test_generate_manual_invalid_version(self):
        with self.assertRaises(ValueError):
            generate_qr_manual("data", 0, "L")
        with self.assertRaises(ValueError):
            generate_qr_manual("data", 41, "L")

    def test_decode_roundtrip(self):
        png_bytes, _ = generate_qr_min_version("roundtrip123", "M")
        decoded = decode_qr(png_bytes)
        self.assertEqual(decoded, "roundtrip123")

if __name__ == '__main__':
    unittest.main()
