################################################Scrapping Multiple Pages Using BeautifulSoup###########################################################


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Start the timer
start_time = time.time()

# Base URL of the website
BASE_URL = "https://kando.tech/investors/all?page="

# Initialize lists to store data
investor_names = []
country_names = []
investor_profile = []
investor_deals = []

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # Delay (in seconds) between retries

# Loop through the pages
for page in range(0, 634):  # Adjust range as needed
    print(f"Scraping page {page + 1}...")
    url = BASE_URL + str(page)

    retries = 0
    while retries < MAX_RETRIES:
        response = requests.get(url)
        if response.status_code == 200:
            # Successfully fetched the page
            break
        else:
            print(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying... ({retries}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)  # Wait before retrying

    # Check if the page was fetched successfully after retries
    if response.status_code != 200:
        print(f"Skipping page {page + 1} after {MAX_RETRIES} retries.")
        continue

    # Parse the HTML using BeautifulSoup
    soup = bs(response.text, "html.parser")
    
    # Find all data elements by class name
    investors = soup.find_all("td", class_="views-field views-field-field-investor")
    countries = soup.find_all("td", class_="views-field views-field-field-country")
    profiles = soup.find_all("td", class_="views-field views-field-field-co-summary")
    deals = soup.find_all("td", class_="views-field views-field-nid views-align-right")
    
    # Append data to respective lists
    for investor, country, profile, deal in zip(investors, countries, profiles, deals):
        investor_names.append(investor.text.strip())
        country_names.append(country.text.strip())
        investor_profile.append(profile.text.strip())
        investor_deals.append(deal.text.strip())

    # Break if no more results are found (end of pagination)
    if not investors:
        print("No more investors found. Ending scrape.")
        break

    # Add a delay between requests to prevent server overload
    time.sleep(2)  # Adjust delay as needed (in seconds)

# Save data to Excel
if investor_names and country_names:
    df = pd.DataFrame({
        "Investor Names": investor_names,
        "Country Names": country_names,
        "Profile": investor_profile,
        "Deals": investor_deals
    })
    df.to_excel("investor_country_data7.xlsx", index=False)
    print("Data saved to 'investor_country_data6.xlsx'.")
else:
    print("No data was scraped.")

# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Time taken to complete the scraping: {elapsed_time:.2f} seconds")



