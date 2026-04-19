from parser import AvitoParser
from storage import CSVStorage
from coordinator import AvitoScraper

if __name__ == "__main__":
    # Dependency Injection
    parser = AvitoParser()
    storage = CSVStorage() 
    
    # Run the scraping process
    scraper = AvitoScraper(parser=parser, storage=storage, pages_to_scrape=3)
    scraper.run()