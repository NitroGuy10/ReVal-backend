import json

INPUT_FILE = "data/Electronics_5_small.json"
OUTPUT_FILE = "data/reviews.json"
FIELD_NAME = "reviewText"


with open(INPUT_FILE) as in_file:
    with open(OUTPUT_FILE, "w") as out_file:
        out_file.write('{"reviews": [\n')
        first = False
        for line in in_file:
            review = json.loads(line)
            if FIELD_NAME in review:
                if not first:
                    first = True
                else:
                    out_file.write(",")
                json.dump(review[FIELD_NAME], out_file)
                out_file.write("\n")
        out_file.write("]}")


