import os
import git
from typing import TypeAlias
import dotenv
import requests
import json

# Global variables for local and remote repo
repoURL = "https://github.com/CVEProject/cvelistV5"
repoLocalPath = os.getcwd() + "/cvelistV5"
repo = git.Repo(repoLocalPath)
repo_origin = repo.remotes.origin
directory_path = "cvelistV5/cves"

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

# Traverse the cve directory and parse each json via preorder DFS
def DFS(start: str) -> None:

    # Utility function for DFS
    def DFSutil(path: str, visited: set) -> None:

        visited.add(path)
        print(f"Visited {path}.")

        # If the file is not a directory, dont read it
        if not os.path.isdir(path):

            # Parse json files here, json files are leaves in the dir tree
            # ---- >  < ---- #
            return

        # If the file is a directory, read it and check if in set
        for file in os.listdir(path):

            full_path = os.path.join(path, file)

            if full_path not in visited:
                DFSutil(full_path, visited)

    visited = set()

    DFSutil(start, visited)


# Compare latest commit from github repo
def compareLocalRemoteCommits() -> dict[str, str]:
    try:

        # Get a commit object for the local repo head
        localHead = repo.head.commit
        print(f"Successfully found local head -> {localHead}.")

        # Fetch to get latest updates, get a commit oject for remote repo head
        repo_origin.fetch()
        remoteHead = repo.refs['origin/main'].commit
        print(f"Successfully found remote head -> {remoteHead}.")


        # If remote has changes, diff and find changed items
        if localHead != remoteHead:

            print("Difference between local and remote, finding modified files.")

            diff = remoteHead.diff(localHead)
            diffItems: Dict[str, str] = {}

            # Return a dictionary of created, modified, or deleted file paths to change type
            for diff_item in diff:
                print(f"{diff_item.a_path} -> {diff_item.change_type}")
                diffItems[diff_item.a_path] = diff_item.change_type
            print(f"Successfull found {len(diffItems)} changes.")

            # Finally, pull updates into local since changes are tracked
            repo_origin.pull()
            print("Successfully pulled repository changes.")
            return diffItems

        # No changes found, return empty dict
        print("Local repository is up to date, no new commits found.")
        return {}


    except subprocess.CalledProcessError as e:
        print(e)
        return {} # Treat error as no changes found




if __name__ == "__main__":

    compareLocalRemoteCommits()



    # DFS(directory_path)