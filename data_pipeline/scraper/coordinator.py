import time
import random
import concurrent.futures
from browser import BrowserManager
from parser import AvitoParser
from storage import DataStorage
from decorators import retry_on_error

class AvitoScraper:
    def __init__(self, parser: AvitoParser, storage: DataStorage, pages_to_scrape=3):
        self.parser = parser
        self.storage = storage
        self.pages_to_scrape = pages_to_scrape
        self.base_url = "https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?o="

    @retry_on_error(retries=3, delay=5)
    def _scrape_single_car(self, link):
        browser = BrowserManager()
        driver = browser.get_driver()
        try:
            print(f"🔄 Scraping: {link}")
            driver.get(link)
            time.sleep(random.uniform(3, 5)) 
            return self.parser.extract_car_details(driver.page_source, link)
        except Exception as e:
            print(f"⚠️ Failed to scrape {link}: {e}")
            return None
        finally:
            browser.quit()

    def run(self):
        # Step 1: Collect Links
        main_browser = BrowserManager()
        driver = main_browser.get_driver()
        all_links = []
        
        for page in range(1, self.pages_to_scrape + 1):
            try:
                print(f"📄 Fetching links from Page {page}...")
                driver.get(f"{self.base_url}{page}")
                time.sleep(random.uniform(2, 4))
                links = self.parser.extract_links(driver.page_source)
                all_links.extend(links)
            except Exception as e:
                print(f"⚠️ Page {page} skipped due to timeout.")
                continue # Skip to next page
                
        main_browser.quit()

        unique_links = list(set(all_links))
        print(f"\n📌 Found {len(unique_links)} unique links. Starting Safe Scraping (1 Worker)...\n")

        # Step 2: Extract Details using 1 worker to save RAM
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(self._scrape_single_car, unique_links))

        scraped_data = [res for res in results if res is not None]
        filename = f"avito_cars_dataset.csv"
        self.storage.save(scraped_data, filename)