import json
import time
import requests
from bs4 import BeautifulSoup

# Load catalog data from stage 1
with open("shl_assessments_paginated.json", "r") as f:
    assessments = json.load(f)

updated_assessments = []

for i, assessment in enumerate(assessments):
    url = assessment["url"]
    print(f"[{i + 1}/{len(assessments)}] Scraping: {url}")

    description = "N/A"
    duration = -1

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all relevant info blocks
        rows = soup.select("div.product-catalogue-training-calendar__row.typ")

        for row in rows:
            heading = row.find("h4")
            if heading:
                heading_text = heading.get_text(strip=True).lower()

                # Extract description
                if "description" in heading_text:
                    desc_p = row.find("p")
                    description = desc_p.get_text(strip=True) if desc_p else "N/A"

                # Extract duration
                elif "assessment length" in heading_text:
                    dur_p = row.find("p")
                    if dur_p:
                        digits = "".join(filter(str.isdigit, dur_p.text))
                        duration = int(digits) if digits else -1

    except Exception as e:
        print(f"⚠️ Failed to scrape {url} due to: {e}")

    assessment["description"] = description
    assessment["duration"] = duration
    updated_assessments.append(assessment)

    time.sleep(0.75)  # Respectful delay

# Save final enriched dataset
with open("shl_assessments_complete.json", "w") as f:
    json.dump(updated_assessments, f, indent=2)

print(f"\n✅ Detail scraping complete. {len(updated_assessments)} assessments enriched.")
