import dotenv
import os
import requests
import json
import datetime
from typing import TypeAlias

# Global variables for easy access later in script
dotenv.load_dotenv()
apiKey = os.getenv("NVD_API_KEY")
headers = {"apiKey": apiKey}
baseURL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
noAffectedVersion = ['CVE-2022-21127', 'CVE-2022-0002']
plainAffectedVersion = ['CVE-2022-21173']

print("------------------ Retrieving CVE with no affected version. ------------------")

for cve in noAffectedVersion:
    url = f"{baseURL}?cveId={cve}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"CVE: {cve}")

        # Write to output file to see the raw api response
        with open(f"nvd_data/{cve}.json", "a") as f:
            json.dump(data, f, indent=2)


    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")