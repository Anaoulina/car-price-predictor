from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserManager:
    def __init__(self):
        self.driver = None

    def get_driver(self):
        if not self.driver:
            options = Options()
            # Optimization strategy: Don't wait for images/ads
            options.page_load_strategy = 'eager' 
            
            options.add_argument("--headless=new") 
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # Disable images to save bandwidth and time
            options.add_argument("--blink-settings=imagesEnabled=false")
            
            options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            
            self.driver = webdriver.Chrome(options=options)
            # Set a shorter timeout but more aggressive strategy
            self.driver.set_page_load_timeout(50) 
            
        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()