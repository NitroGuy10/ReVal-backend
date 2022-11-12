
INPUT_FILE = "data/Electronics_5.json"
OUTPUT_FILE = "data/Electronics_5_small.json"

with open(INPUT_FILE) as in_file:
    with open(OUTPUT_FILE, "w") as out_file:
        for line_num in range(0, 100000):
            out_file.write(in_file.readline())
