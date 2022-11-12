
with open("Electronics_5.json") as in_file:
    with open("Electronics_5_small.json", "w") as out_file:
        for line_num in range(0, 100000):
            out_file.write(in_file.readline())
