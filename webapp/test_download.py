import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDownloadQR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome options for headless and download
        cls.download_dir = os.path.abspath("downloads")
        os.makedirs(cls.download_dir, exist_ok=True)
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': cls.download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.base_url = "http://localhost:8002/smallqr/"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_download_qr(self):
        driver = self.__class__.driver
        base_url = self.__class__.base_url
        download_dir = self.__class__.download_dir
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Fill the form with dummy text
        link_input = wait.until(EC.presence_of_element_located((By.ID, "link")))
        dummy_text = "dummy test text"
        link_input.send_keys(dummy_text)

        # Solve the captcha
        captcha_input = driver.find_element(By.ID, "captcha")
        question = captcha_input.get_attribute("placeholder")
        import re
        nums = re.findall(r"(\d+)", question)
        answer = str(int(nums[0]) + int(nums[1]))
        captcha_input.send_keys(answer)

        # Submit the form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        try:
            submit_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", submit_btn)

        # Wait for the QR code result card to appear (ensures page transition is done)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))

        # Wait for the download button to appear and be clickable
        download_btn = wait.until(EC.element_to_be_clickable((By.ID, "downloadBtn")))
        self.assertTrue(download_btn.is_displayed(), "Download button not displayed")

        # Check that the QR code image is present
        qr_img = wait.until(EC.presence_of_element_located((By.ID, "qrImage")))
        self.assertTrue(qr_img.is_displayed(), "QR code image not displayed")

        # Scroll download button into view and click
        driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
        download_btn.click()

        # Wait for file to appear in download dir
        time.sleep(2)  # Give time for download
        files = os.listdir(download_dir)
        self.assertTrue(any(f.endswith('.png') for f in files), "QR code PNG not downloaded")

if __name__ == "__main__":
    unittest.main()
