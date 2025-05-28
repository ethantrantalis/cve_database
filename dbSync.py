import sqlite3
import json
import pandas as pd
import os

# Establish database connection and interaction
con = sqlite3.connect('nvd.sqlite')
cursor = con.cursor()

def parseJson(filePath: str) -> None:


    for file in os.listdir(filePath):

        with open(f"{filePath}{file}", "r") as f:

            products = json.load(f)['products']
            for product in products:
                if 'titles' in product['cpe']:
                    del product['cpe']['titles']








parseJson("cpe_data/")
