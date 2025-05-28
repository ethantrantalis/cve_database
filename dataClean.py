import os
import pandas as pd
import json
from typing import List, Dict
import csv


def cleanJSON(inputs: List[dict], attributes: List[str]) -> List[dict]:
    return [{k: v for k, v in i.items() if k in attributes}
            for i in inputs]


def JSONtoCSV(inputs: List[dict], output: str, header: int) -> None:

    with open(output, "a") as f:
        writer = csv.DictWriter(f, fieldnames=inputs[0].keys())
        writer.writeheader()
        writer.writerows(inputs)


with open("cpe_data/cpe0To9999.json", "r") as f:
    data = json.load(f)["products"]
    temp = []
    for d in data:

        temp.append(d["cpe"])

JSONtoCSV(cleanJSON(temp, ["deprecated", "cpeName","cpeNameId", "lastModified", "created"]), "cpeClean.csv")
