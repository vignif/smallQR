import unittest
from webapp.app import app


DOWNLOAD_LABEL_FRAGMENT = b'Download'  # button text changed in UI

class SmallQRTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        response = self.app.get('/smallqr/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'smallQR', response.data)

    def test_create_qr_code_default_min_version(self):
        # Get captcha question from GET
        resp = self.app.get('/smallqr/')
        self.assertEqual(resp.status_code, 200)
        # Extract captcha answer from session
        with self.app.session_transaction() as sess:
            captcha_answer = sess['captcha_answer']
        data = {
            'link': 'https://example.com',
            'check': 'L',
            'version': '0',  # trigger minimal version path
            'captcha': captcha_answer,
            'captcha_question': f'What is {captcha_answer}?'  # Not used in validation
        }
        post_response = self.app.post('/smallqr/', data=data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(DOWNLOAD_LABEL_FRAGMENT, post_response.data)
        # Minimal version label or 'Minimal' word should appear when auto mode used
        self.assertIn(b'Minimal', post_response.data)

    def test_create_qr_code_invalid_captcha(self):
        self.app.get('/smallqr/')
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

    def test_create_qr_code_with_explicit_version(self):
        self.app.get('/smallqr/')
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
        self.assertIn(b'Version', post_response.data)
        self.assertIn(DOWNLOAD_LABEL_FRAGMENT, post_response.data)

    def test_create_qr_code_too_long(self):
        self.app.get('/smallqr/')
        with self.app.session_transaction() as sess:
            captcha_answer = sess['captcha_answer']
        long_input = 'x' * (app.config['MAX_INPUT_LENGTH'] + 1)
        data = {
            'link': long_input,
            'check': 'L',
            'version': '0',
            'captcha': captcha_answer,
            'captcha_question': f'What is {captcha_answer}?'
        }
        post_response = self.app.post('/smallqr/', data=data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'Input exceeds maximum length', post_response.data)

if __name__ == '__main__':
    unittest.main()
