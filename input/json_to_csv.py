import json
import csv

INPUT_FILE = "data/Electronics_5_small.json"
OUTPUT_FILE = "data/Electronics_5_small.csv"
FIELDS = [
    # (input json field name, output csv field name)
    ("overall" , "rating"),
    ("vote", "reviewer_upvotes"),
    ("asin", "item_name"),
    ("reviewerName", "reviewer_name"),
    ("summary", "review_summary"),
    ("reviewText", "review_text"),
    ("unixReviewTime", "unix_review_time")
]

### UHHHHHHHHHHHHHHHHHHHHHH this don't work

with open(INPUT_FILE) as in_file:
    # review = json.loads(in_file.readline())
    # print(json.dumps(review, indent="    "))
    json_fields = [field[0] for field in FIELDS]
    csv_fields = [field[1] for field in FIELDS]

    with open(OUTPUT_FILE, "w") as out_file:
        # Dictionary CSV header
        out_file.write(",".join(json_fields) + "\n")
        writer = csv.DictWriter(out_file, fieldnames=csv_fields)
        for line in in_file:
            review = json.loads(line)
            valid_review = True
            for field in review:
                if field not in csv_fields:
                    del review[field]
            for field in FIELDS:
                if field[0] not in review:
                    valid_review = False
                    break
            if valid_review:
                writer.writerow(review)

