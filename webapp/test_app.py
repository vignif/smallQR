import unittest
from webapp.app import app

class SmallQRTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        response = self.app.get('/smallqr/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'smallQR', response.data)

    def test_create_qr_code_default(self):
        # Get captcha question from GET
        get_response = self.app.get('/smallqr/')
        self.assertEqual(get_response.status_code, 200)
        # Extract captcha answer from session
        with self.app.session_transaction() as sess:
            captcha_answer = sess['captcha_answer']
        data = {
            'link': 'https://example.com',
            'check': 'L',
            'captcha': captcha_answer,
            'captcha_question': f'What is {captcha_answer}?'  # Not used in validation
        }
        post_response = self.app.post('/smallqr/', data=data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'QR encoding results', post_response.data)
        self.assertIn(b'Download QR Code', post_response.data)

    def test_create_qr_code_invalid_captcha(self):
        get_response = self.app.get('/smallqr/')
        with self.app.session_transaction() as sess:
            captcha_answer = sess['captcha_answer']
        data = {
            'link': 'https://example.com',
            'check': 'L',
            'captcha': 'wrong',
            'captcha_question': f'What is {captcha_answer}?'
        }
        post_response = self.app.post('/smallqr/', data=data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'Captcha answer is incorrect', post_response.data)

    def test_create_qr_code_with_version(self):
        get_response = self.app.get('/smallqr/')
        with self.app.session_transaction() as sess:
            captcha_answer = sess['captcha_answer']
        data = {
            'link': 'test123',
            'check': 'H',
            'version': '5',
            'captcha': captcha_answer,
            'captcha_question': f'What is {captcha_answer}?'
        }
        post_response = self.app.post('/smallqr/', data=data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'QR encoding results', post_response.data)
        self.assertIn(b'Version', post_response.data)

if __name__ == '__main__':
    unittest.main()
