import json
import time
import logging
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Initialize logging infrastructure
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class JobScraper:
    def __init__(self, storage_dir="data", filename="job_listings.json"):
        self.storage_dir = Path(storage_dir)
        self.file_path = self.storage_dir / filename
        
        # Target endpoint (Reliable Sandbox Platform for Testing Scrapers)
        self.target_url = "https://realpython.github.io/fake-jobs/"
        
        # Mimic standard organic web browser headers to bypass automated barriers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_html(self) -> str:
        """Downloads the raw HTML stream from the target network endpoint."""
        try:
            logging.info(f"Injecting HTTP GET request to endpoint: {self.target_url}")
            response = requests.get(self.target_url, headers=self.headers, timeout=10)
            
            # Explicitly raise an error if HTTP response status is not 200 OK
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Network transport error encountered: {e}")
            raise

    def parse_listings(self, html_content: str) -> list:
        """Parses the raw HTML document and isolates key data vectors using BeautifulSoup."""
        logging.info("Initializing DOM structural parser...")
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Isolate the main results container element
        results_container = soup.find(id="ResultsContainer")
        if not results_container:
            logging.error("Target node framework placeholder structural IDs missing.")
            return []

        # Find all structural cards wrapping specific job listings
        job_cards = results_container.find_all("div", class_="card-content")
        extracted_jobs = []

        for index, card in enumerate(job_cards):
            try:
                # Targeted data extraction via structural class parsing
                title_element = card.find("h2", class_="title")
                company_element = card.find("h3", class_="company")
                location_element = card.find("p", class_="location")
                date_element = card.find("time")
                
                # Extract link safely from the action card footer
                link_element = card.find_all("a")[1] # Second anchor tag on card is the apply link
                apply_link = link_element["href"] if link_element else "N/A"

                # Standardize strings, cleaning whitespace and terminal characters
                job_data = {
                    "id": index + 1,
                    "title": title_element.text.strip() if title_element else "N/A",
                    "company": company_element.text.strip() if company_element else "N/A",
                    "location": location_element.text.strip() if location_element else "N/A",
                    "date_posted": date_element.text.strip() if date_element else "N/A",
                    "apply_url": apply_link
                }
                
                extracted_jobs.append(job_data)
            except Exception as item_err:
                logging.warning(f"Skipping damaged record element matrix node at index {index}: {item_err}")
                continue
                
        return extracted_jobs

    def save_to_json(self, data: list):
        """Persists the extracted dataset structure to an ordered JSON disk file."""
        try:
            self.storage_dir.mkdir(exist_ok=True)
            
            with open(self.file_path, "w", encoding="utf-8") as json_file:
                # Save with clean structural indents for production readability
                json.dump(data, json_file, indent=4, ensure_ascii=False)
                
            logging.info(f"Data storage successful! Wrapped records written out to: {self.file_path}")
        except IOError as io_err:
            logging.error(f"Failed writing data payload block matrix down to local storage: {io_err}")
            raise

    def run_pipeline(self):
        """Orchestrates the extraction, transformation, and storage pipeline."""
        start_time = time.time()
        try:
            html = self.fetch_html()
            jobs_list = self.parse_listings(html)
            
            if jobs_list:
                self.save_to_json(jobs_list)
                logging.info(f"Pipeline executed successfully. Harvested {len(jobs_list)} records in {time.time() - start_time:.2f}s")
            else:
                logging.warning("Pipeline terminated. Output array empty.")
        except Exception as global_err:
            logging.error(f"Pipeline processing failed: {global_err}")