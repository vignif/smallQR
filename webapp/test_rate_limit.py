import unittest
from webapp.app import app

class TestRateLimit(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_ping_rate_limit(self):
        # Allowed 5 per minute, 6th should 429
        statuses = []
        for i in range(5):
            r = self.client.get('/ping')
            statuses.append(r.status_code)
            self.assertEqual(r.status_code, 200)
        sixth = self.client.get('/ping')
        self.assertEqual(sixth.status_code, 429, f"Expected 429 on 6th call, got {sixth.status_code}")
        # Confirm limiter headers present
        self.assertIn('Retry-After', sixth.headers)

if __name__ == '__main__':
    unittest.main()
