import dotenv
import os
import requests
import json

# Global variables for easy access later in the script
dotenv.load_dotenv()
apiKey = os.getenv("API_KEY")
headers = {"apiKey": apiKey}
baseURL = "https://services.nvd.nist.gov/rest/json/"



def cveExample() -> None:

    noAffectedVersion = ['CVE-2022-21127', 'CVE-2022-0002']
    plainAffectedVersion = ['CVE-2022-21173']

    for cve in noAffectedVersion:
        url = f"{baseURL}cves/2.0?cveId={cve}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"CVE: {cve}_v2")

            # Write to an output file to see the raw api response
            with open(f"cve_data/{cve}.json", "a") as f:
                json.dump(data, f, indent=2)


        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")

def cveIndexExample() -> None:

    url = f"{baseURL}cves/2.0/?resultsPerPage=2000&startIndex=0"
    try:
        headers={"apiKey": apiKey}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        with open("cve_data/cveIndex0To2000.json", "a") as f:
            json.dump(data, f, indent=2)

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")

def cpeExample() -> None:


    url = f"{baseURL}cpes/2.0/?resultsPerPage=10000&startIndex=0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open("cpe_data/cpeIndex0To10000.json", "a") as f:
            json.dump(data, f, indent=2)

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    cveIndexExample()


