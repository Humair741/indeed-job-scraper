import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Load environment variables
chrome_driver_path = os.getenv('CHROME_DRIVER_PATH', 'default/path/to/chromedriver')
brave_binary_location = os.getenv('BRAVE_BINARY_LOCATION', 'default/path/to/brave')

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = brave_binary_location

service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with the Brave browser and ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape job postings from Indeed
def scrape_jobs():
    # Create an empty DataFrame to store job postings
    df = pd.DataFrame(columns=['Link', 'Job Title', 'Company', 'Date Posted', 'Location'])

    while True:
        try:
            # Wait until the job postings are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'lxml')
            boxes = soup.find_all('div', class_='job_seen_beacon')

            # Extract job details from each posting
            for i in boxes:
                link_element = i.find('a')
                job_title_element = i.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
                company_element = i.find('span', class_='css-63koeb eu4oa1w0')
                location_element = i.find('div', class_='css-1p0sjhy eu4oa1w0')
                date_posted_element = i.find('span', class_='css-qvloho eu4oa1w0')

                # Retrieve job details or set default values
                link = link_element.get('href') if link_element else 'N/A'
                job_title = job_title_element.text if job_title_element else 'N/A'
                company = company_element.text if company_element else 'N/A'
                location = location_element.text if location_element else 'N/A'
                date_posted = date_posted_element.text if date_posted_element else 'N/A'

                # Append job details to the DataFrame
                df = pd.concat([df, pd.DataFrame([{'Link': link, 'Job Title': job_title, 'Company': company, 'Date Posted': date_posted, 'Location': location}])], ignore_index=True)

            # Try to find the "Next Page" link and navigate to it
            next_page_element = soup.find('a', {'aria-label': 'Next Page'})
            if next_page_element:
                next_page = next_page_element.get('href')
                next_page = 'https://ca.indeed.com' + next_page
                driver.get(next_page)
                time.sleep(3)  # Adjust this if necessary
            else:
                print("Next page element not found.")
                break  # Exit the loop if no next page is found

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Data-Cleaning
    df['Link'] = 'https://ca.indeed.com' + df['Link']

    def posted(x):
        x = x.replace('PostedPosted', '').strip()
        return x

    df = df.iloc[1:, :]  # Remove the first row

    def day(x):
        try:
            x = x.replace('days ago', '').strip()
            x = x.replace('day ago', '').strip()
            return float(x)
        except:
            return x

    df['Date Posted'] = df['Date Posted'].apply(posted)
    df['Date Posted'] = df['Date Posted'].apply(day)

    # Save the DataFrame to a CSV file
    df.to_csv('indeed_jobs.csv', index=False)
    print("Data saved to indeed_jobs.csv")

# Start the scraping process
driver.get("https://ca.indeed.com/")
scrape_jobs()

# Close the WebDriver
driver.quit()
