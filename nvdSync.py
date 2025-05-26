import dotenv
import os
import requests
import json
import time

# Load env for api key
# ----> ADD A .env file with API_KEY="" <----
dotenv.load_dotenv()
apiKey = os.getenv("API_KEY")
headers = {"apiKey": apiKey}
baseURL = "https://services.nvd.nist.gov/rest/json/"

# Helper to get the total results from an initial pull for future db initializations
def getTotalResults(filePath: str) -> int:

    # Return the value found at totalResults or -1 if error
    try:
        with open(filePath, "r") as f:
            data = json.load(f)

            return data["totalResults"]

    except FileNotFoundError:
        return -1

# Helper function to call api for a variety of different api URLs
def callAPI(url: str, startIndex: int, callType: str, resultsPerPage: int) -> int:

    # Return new startIndex value after successful API call or -1
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        with open(f"{callType.lower()}_data/{callType.lower()}{startIndex}To{startIndex + resultsPerPage -1}.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"Successfully pulled {len(data.get('vulnerabilities', []))} {callType.lower()}s up to index {startIndex + resultsPerPage -1}.")

        return startIndex + resultsPerPage  # Return the start index incremented by how many records were called

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")

        return -1  # Error return

# Function to pull all records as per the rate limiter on nvd 50 calls per 30 secs w/ apiKey
def getRecords(callType: str, resultsPerPage: int) -> None:

    # Return None since helper functions handle errors

    # According to the documentation, the max CVEs per request are 2000
    # Set start to 0, pulling 2000 record increments
    startIndex = 0
    os.makedirs(f"{callType.lower()}_data", exist_ok=True)  # Make the output directory if not found
    url = f"{baseURL}{callType.lower()}s/2.0/?resultsPerPage={resultsPerPage}&startIndex={startIndex}"
    startIndex = callAPI(url, startIndex, callType, resultsPerPage)

    if startIndex == -1:
        print("Error: Failed to pull records.")
        return

    totalResults = getTotalResults(f"{callType.lower()}_data/{callType.lower()}{startIndex - resultsPerPage}To{startIndex -1}.json")
    while startIndex < totalResults:

        # Pause api calls to adhere to nvd rate limiter
        time.sleep(1)

        # Update URL with new startIndex from previous callAPI
        url = f"{baseURL}{callType.lower()}s/2.0/?resultsPerPage={resultsPerPage}&startIndex={startIndex}"
        startIndex = callAPI(url, startIndex, callType, resultsPerPage)


        if startIndex == -1:
            print("Error: Failed to pull records.")
            break



if __name__ == "__main__":
    getRecords("CPE", 10000)