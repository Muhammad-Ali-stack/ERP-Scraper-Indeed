import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

erp_keywords = [
    "SAP", "Oracle", "Microsoft Dynamics", "Netsuite",
    "Infor", "Epicor", "Sage", "Workday"
]

countries = {
    "UK": "united-kingdom",
    "Ireland": "ireland",
    "Germany": "germany",
    "France": "france",
    "Italy": "italy",
    "Spain": "spain",
    "Sweden": "sweden",
    "Norway": "norway",
    "Denmark": "denmark",
    "Finland": "finland"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

results = []
total_jobs_collected = 0
job_limit = 50  # Set your desired total job limit

for country_name, country_code in countries.items():
    for keyword in erp_keywords:
        if total_jobs_collected >= job_limit:
            break

        query = f"{keyword} site:linkedin.com/jobs"
        url = f"https://www.google.com/search?q={query}+{country_code}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            job_count = sum(1 for link in links if "linkedin.com/jobs" in link.get("href", ""))
            
            # Limit remaining jobs if over limit
            jobs_to_add = min(job_count, job_limit - total_jobs_collected)
            total_jobs_collected += jobs_to_add

            print(f"[{country_name}] {keyword}: {jobs_to_add} jobs added (Total: {total_jobs_collected})")

            results.append({
                "Country": country_name,
                "ERP": keyword,
                "Estimated LinkedIn Job Count": jobs_to_add
            })

            time.sleep(2)  # Avoid rate limiting
        except Exception as e:
            print(f"❌ Error fetching jobs for {keyword} in {country_name}: {e}")
            results.append({
                "Country": country_name,
                "ERP": keyword,
                "Estimated LinkedIn Job Count": 0
            })

    if total_jobs_collected >= job_limit:
        break

# Save to Excel
df = pd.DataFrame(results)
df.to_excel("linkedin_erp_jobs_limited.xlsx", index=False)
print("✅ Done. 50 jobs collected and saved to linkedin_erp_jobs_limited.xlsx")
