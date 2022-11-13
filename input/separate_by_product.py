

import json
import shutil
import os

INPUT_FILE = "data/Electronics_5_small.json"
OUTPUT_DIRECTORY = "data/by_product/"
FIELD_NAME = "asin"
ONE_JSON_OBJECT = True

if os.path.exists(OUTPUT_DIRECTORY):
    shutil.rmtree(OUTPUT_DIRECTORY)
os.mkdir(OUTPUT_DIRECTORY)

products = set()

with open(INPUT_FILE) as in_file:
    for line in in_file:
        review = json.loads(line)
        if "asin" in review:
            with open(os.path.join(OUTPUT_DIRECTORY, review["asin"] + ".json"), "a") as out_file:
                if ONE_JSON_OBJECT:
                    if review["asin"] in products:
                        out_file.write(",")
                    else:
                        # out_file.write('{"reviews": [\n')
                        out_file.write('[\n')
                        products.add(review["asin"])
                json.dump(review, out_file)
                out_file.write("\n")

if ONE_JSON_OBJECT:
    for product in products:
        with open(os.path.join(OUTPUT_DIRECTORY, product + ".json"), "a") as out_file:
            # out_file.write("]}")
            out_file.write("]")


