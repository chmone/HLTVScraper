import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from HLTVScraper.methods.utility.parse import get_parsed_page

class parse:
    
    def get_parsed_page(url):
        # Set up the Firefox options for headless mode
        options = Options()
        options.add_argument("--headless")
        
        # Initialize the Firefox WebDriver
        driver = webdriver.Firefox(options=options)
        
        # Navigate to the URL
        driver.get(url)

        # Delay to allow the page to load fully
        time.sleep(random.uniform(3, 5))  # Random delay between 1-3 seconds

        try:
            # Find and click the 'Accept Cookies' button
            cookie_button = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
            cookie_button.click()

            # Delay after clicking the cookie consent button to allow the page to reload
            #time.sleep(random.uniform(1, 2))  # Random delay between 1-2 seconds
            driver.save_screenshot("datacamp.png")
        except Exception as e:
            print(f"Error clicking cookie consent: {e}")
        
        # Get the page source after interaction
        html_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(html_source, 'html.parser')
        
        # Quit the WebDriver session after scraping
        driver.quit()

        return soup

    #Function to run multiple URLs concurrently
    def scrape_urls_concurrently(urls, max_workers=4):
        results = []
        i = 1
        # Use ThreadPoolExecutor to handle multiple threads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all URLs as tasks to the executor
            futures = {executor.submit(get_parsed_page, url): url for url in urls}
            
            for future in as_completed(futures):
                url = futures[future]
                try:
                    soup = future.result()  # Get the BeautifulSoup object from the task
                    print_str = f"({i}/{len(urls)}) - Successfully scraped {url}"
                    print(print_str)
                    results.append([soup, url])
                    i+=1
                    # Global delay between requests to avoid rate limiting
                    time.sleep(random.uniform(2, 5))  # Random delay between 2-5 seconds

                except Exception as e:
                    print(f"Error scraping {url}: {e}")
        
        return results