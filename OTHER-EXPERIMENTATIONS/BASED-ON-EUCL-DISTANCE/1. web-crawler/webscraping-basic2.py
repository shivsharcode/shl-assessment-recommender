import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
    YES I LOVE TO WRTIE COMMENTS, THESE AREN'T AI-WRITTEN :)
"""

# Setting Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless") # Runs in background
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=options)

# OPEN SHL CATALOG PAGE
base_url = "https://www.shl.com"
page_template = base_url + "/products/product-catalog/?start={}&type=1"


assessments = []
start = 0
step = 12


while True:
    url = page_template.format(start)
    driver.get(url)
    time.sleep(8) # wait for JS to load fully
    
    # parse the loaded page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select("table tbody tr[data-entity-id]")
    
    if not rows:
        break  # Exit loop if no more data found
    
    print(f"Scraping page starting at {start}...")
    
    for row in rows:
        try:
            # Assessment Name & URL
            a_tag = row.select_one("td.custom__table-heading__title a")
            name = a_tag.text.strip()
            rel_url = a_tag['href'].strip()
            full_url = base_url + rel_url
            
            # Remote testing: check if circle with -yes class exists in 2nd <td>
            remote_td = row.select("td")[1]
            remote = bool(remote_td.select_one("span.catalogue__circle.-yes"))
            
            # Adaptive testing : check if the circle with -yes exists in 3rd <td>
            adaptive_td = row.select("td")[2]
            adaptive = bool(adaptive_td.select_one("span.catalogue__circle.-yes"))
            
            # Test type
            test_type_td = row.select("td")[3]
            types = [span.text.strip() for span in test_type_td.select("span.product-catalogue__key")]
            
            assessments.append({
                "name": name,
                "url": full_url,
                "remote_testing": remote,
                "adaptive_testing": adaptive,
                "test_types": types
            })
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
        
    start += step  # Move to the next page
    
# CLEAN UP
driver.quit()

# SAVE TO JSON
with open("shl_assessments_paginated.json", "w") as f:
    json.dump(assessments, f, indent=2)
    


print(f"\n✅ Done. Total assessmennts scraped : {len(assessments)} assessments.")