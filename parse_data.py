import os
import requests
import datetime
from dotenv import load_dotenv


def DFS(start: str):

    def DFSutil(path: str, visited: set):

        visited.add(path)
        print(f"Visited {path}")

        # If the file is not a directory, dont read it
        if not os.path.isdir(path):
            return

        # If the file is a directory, read it and check if in set
        for file in os.listdir(path):

            full_path = os.path.join(path, file)

            if full_path not in visited:
                DFSutil(full_path, visited)

    visited = set()

    DFSutil(start, visited)

def pullLatestTime():
    # Pull latest time from github repo
    owner = "CVEProject"
    project = "cvelistV5"

    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{project}")

    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)

    latest_update = datetime.datetime.fromisoformat(response.json()["updated_at"]).isoformat()

    return latest_update

if __name__ == "__main__":

    if os.path.isfile(".env"):
        load_dotenv()

    else:

        with open(".env", "a") as f:

            f.write(f"LAST_UPDATE_TIME=\"{pullLatestTime()}\"")


    load_dotenv()

    print(os.getenv("LAST_UPDATE_TIME"))

    directory_path = "cvelistV5/cves"
    # DFS(directory_path)