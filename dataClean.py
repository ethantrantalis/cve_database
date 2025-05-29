import os
import pandas as pd
import json
from typing import List, Dict
import csv


def cleanJSON(inputs: List[dict], attributes: List[str]) -> List[dict]:
    return [{k: v for k, v in i.items() if k in attributes}
            for i in inputs]


def JSONtoCSV(target: str, output: str, entriesField: str, callType: str, attributes: List[str]) -> None:

    with open(output, "a") as f:

        # Prepare the csv file with header
        writer = csv.DictWriter(f, fieldnames=attributes)
        writer.writeheader()

        # Get the target json files
        json_files = [js for js in os.listdir(target) if js.endswith(".json")]


        # For each json file, get the data, and create a list of all records
        for js in json_files:

            try:

                # Get the data based on the entriesField of that record type
                data = json.load(open(os.path.join(target, js), "r"))[entriesField]

                # Format a list of records for csv writing
                cleaned = cleanJSON([d[callType.lower()] for d in data], attributes)

                # Write each dict to the csv
                map(lambda i: writer.writerow(i), cleaned)

            except json.decoder.JSONDecodeError:
                print("JSON decoder error")
                continue







JSONtoCSV("cpe_data", "cpe_cleaned.csv", "products", "CPE", ["deprecated", "cpeName","cpeNameId", "lastModified", "created"])


