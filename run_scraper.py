from scraper import JobScraper

def main():
    print("==========================================")
    print("   AUTOMATED ETL JOB SCRAPER DISPATCHER  ")
    print("==========================================\n")
    
    # Initialize the automated system execution pipeline
    scraper = JobScraper()
    scraper.run_pipeline()
    
    print("\n[System Check]: Operation fully closed.")

if __name__ == "__main__":
    main()