import json
import psycopg2
from psycopg2 import sql
from datetime import datetime


def process_jsons(files):
    for f in files:
        with open('../data/' + f) as json_file:
            data = json.load(json_file)

            data = data["results"][0]["members"]

            for entry in data:
               print(json.dumps(data, sort_keys=True, indent=4))


def main():
    process_jsons(['116th-house.json'])


if __name__ == "__main__":
    main()



