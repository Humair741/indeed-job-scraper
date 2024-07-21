# indeed-job-scraper

This Python script scrapes job postings from the Indeed website using Selenium and BeautifulSoup. It extracts job details and saves them into a CSV file for further analysis.

## Features

- **Web Scraping:** Automatically navigates through multiple pages of job postings.
- **Data Extraction:** Collects job title, company, location, date posted, and job link.
- **CSV Export:** Saves the scraped data into a CSV file named `indeed_jobs.csv`.

## Modules Used

- **BeautifulSoup:** For parsing HTML and extracting job details.
- **Selenium:** For automating web browsing and navigating through pages.
- **pandas:** For managing and saving the scraped data.
- **time:** For handling delays between page loads.

## How to Use

1. **Install Dependencies:**
   Ensure you have the required Python packages installed. You can install them using pip:

   ```bash
   pip install beautifulsoup4 selenium pandas
