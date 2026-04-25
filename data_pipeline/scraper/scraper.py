
import csv
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


from decorators import retry, log_step, random_delay, timer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


class AvitoCarScraper:

    
    def __init__(self, total_pages: int = 5, output_path: str = "cars_avito.csv"):
        
        self.total_pages = total_pages
        self.output_path = output_path
        self.driver = None  
        self.all_listings = []  #accumulate the car data
    
    @timer 
    @log_step 
    def build_driver(self) -> webdriver.Chrome:
        
        #user-agent to avoid detection
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
        ]
        ua = random.choice(user_agents)
        log.info(f"Using User-Agent: {ua[:50]}...")
        
        #steps to acces the ebrowser
        opts = Options()
        opts.add_argument(f"user-agent={ua}")  
        opts.add_argument("--start-maximized") 
        opts.add_argument("--disable-blink-features=AutomationControlled") 
        opts.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        
        
        driver = webdriver.Chrome(options=opts)
        
       
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        return driver
    
    @retry(max_attempts=3, delay=4.0) 
    @random_delay(min_s=2.5, max_s=5.5)  
    @log_step  
    def navigate_to_page(self, page: int) -> bool:
    
        
        if page == 1:
            url = "https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre"
        else:
            url = f"https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre?o={page}"
        
        log.info(f"Loading page {page}: {url}")
        self.driver.get(url)
        
       
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.sc-1jge648-0")))
        
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 0);")
        
        return True
    
    def extract_car_data(self, card) -> dict:
        
        car_title = "N/A"
        title_elem = card.find("p", class_="iHApav")
        if title_elem:
            car_title = title_elem.get_text(strip=True)
        
        #EXTRACT PRICE
        price = "N/A"
        price_span = card.find("span", class_="PuYkS")
        if price_span:
            price = price_span.get_text(strip=True).replace("\u202f", " ")
        
        #EXTRACT VEHICLE DETAILS (Year, Mileage, Transmission, Fuel)
        details_container = card.find("div", class_="sc-b57yxx-2")
        year = mileage = transmission = fuel = "N/A"
        
        if details_container:
           
            detail_spans = details_container.find_all("span", class_="sc-1s278lr-0")
            for span in detail_spans:
                title_span = span.find("span", title=True)
                if title_span:
                    title_attr = title_span.get("title", "")
                    text = span.get_text(strip=True)
                    
                    if "Année-Modèle" in title_attr:
                        year = text
                    elif "Kilométrage" in title_attr:
                        mileage = text
                    elif "Boite de vitesses" in title_attr:
                        transmission = text
                    elif "Type de carburant" in title_attr:
                        fuel = text
        
        #EXTRACT LOCATION
        location = "N/A"
        location_div = card.find("div", class_="sc-b57yxx-13")
        if location_div:
            location_p = location_div.find("p", class_="sc-1x0vz2r-0")
            if location_p:
                location = location_p.get_text(strip=True)
                location = location.replace("Voitures d'occasion dans ", "")
        
        #EXTRACT SELLER NAME
        seller = "N/A"
        seller_div = card.find("div", class_="sc-5rosa-6")
        if seller_div:
            seller_p = seller_div.find("p", class_="sc-1x0vz2r-0")
            if seller_p:
                seller = seller_p.get_text(strip=True)
        
        #EXTRACT AD LINK
        link = "N/A"
        link_elem = card.find("a", href=True)
        if link_elem:
            href = link_elem.get("href", "")
            if href.startswith("/"):
                link = f"https://www.avito.ma{href}"
            else:
                link = href
        
        #EXTRACT POSTING TIME
        post_time = "N/A"
        time_div = card.find("div", class_="sc-5rosa-2")
        if time_div:
            time_p = time_div.find("p", class_="sc-1x0vz2r-0")
            if time_p:
                post_time = time_p.get_text(strip=True)
        
       
        is_shop = bool(card.find("svg", class_="lmuEmf"))
        is_premium = bool(card.find("div", string="Premium"))
        is_urgent = "Urgent" in card.get_text()
        
        # Return a clean dictionary with all extracted data
        return {
            "car_brand_model": car_title,
            "price_dh": price,
            "year": year,
            "mileage_km": mileage,
            "transmission": transmission,
            "fuel_type": fuel,
            "location": location,
            "seller_name": seller,
            "posted": post_time,
            "is_shop": "Yes" if is_shop else "No",
            "is_premium": "Yes" if is_premium else "No",
            "is_urgent": "Yes" if is_urgent else "No",
            "ad_link": link
        }
    
    @log_step  
    def parse_page(self, html: str) -> list:
        
        soup = BeautifulSoup(html, "html.parser")
        
        cards = soup.find_all("a", class_="sc-1jge648-0")
        log.info(f"Found {len(cards)} car listing cards")
        
        # Extract data from each card
        listings = []
        for card in cards:
            try:
                car_data = self.extract_car_data(card)

                if car_data["car_brand_model"] != "N/A":
                    listings.append(car_data)
            except Exception as e:
                log.debug(f"Error parsing card: {e}")
                continue
        
        return listings
    
    @log_step 
    def save_to_csv(self):
        if not self.all_listings:
            log.warning("No data to save!")
            return
        
        fieldnames = ["car_brand_model", "price_dh", "year", "mileage_km", 
                      "transmission", "fuel_type", "location", "seller_name", 
                      "posted", "is_shop", "is_premium", "is_urgent", "ad_link"]
        
        
        with open(self.output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()  
            writer.writerows(self.all_listings) 
        
        log.info(f"Saved {len(self.all_listings)} listings to {self.output_path}")
    
    @timer  
    @log_step 
    def run(self):
        
        log.info("=" * 60)
        log.info("Avito.ma Car Scraper - Starting")
        log.info(f"Pages to scrape: {self.total_pages}")
        log.info(f"Output file: {self.output_path}")
        log.info("=" * 60)
        
        
        self.driver = self.build_driver()
        
        try:
            # Loop through each page
            for page in range(1, self.total_pages + 1):
                log.info(f"\n{'─'*50}")
                log.info(f"PAGE {page}/{self.total_pages}")
                log.info(f"{'─'*50}")
                
                self.navigate_to_page(page)
                
                html = self.driver.page_source
                
                page_listings = self.parse_page(html)
                
                self.all_listings.extend(page_listings)
                log.info(f"Page {page}: {len(page_listings)} cars | Total: {len(self.all_listings)}")
                
                #  delay 
                if page < self.total_pages:
                    delay = random.uniform(3, 6)
                    log.info(f"Waiting {delay:.1f} seconds before next page...")
                    time.sleep(delay)
                    
        except KeyboardInterrupt:
            log.warning("\n Interrupted by user - saving partial results...")
        except Exception as e:
            log.error(f"Error: {e}")
        finally:
            
            if self.driver:
                self.driver.quit()
                log.info("Browser closed.")
        
        
        self.save_to_csv()
        
        
        log.info("\n" + "=" * 60)
        log.info(f"SCRAPING COMPLETE!")
        log.info(f"Total cars extracted: {len(self.all_listings)}")
        log.info(f"Saved to: {self.output_path}")
        
        if self.all_listings:
            log.info("\n SAMPLE DATA (first car):")
            sample = self.all_listings[0]
            for key, value in sample.items():
                log.info(f"   {key}: {value}")
        
        log.info("=" * 60)



if __name__ == "__main__":
    
    scraper = AvitoCarScraper(total_pages=9, output_path="cars_avito.csv")
    scraper.run()