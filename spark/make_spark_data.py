import random

with open('names.txt') as input_file:
    data_size = 10
    with open("./data/data_{}.txt".format(data_size), "w+") as output_file:
        # compile list of names from input_file
        names = []
        for line in input_file:
            items = line.split(" ")

            names.append(items[0])

        # assign random names a random product id
        for i in range(data_size):
            output_file.write(names[random.randint(0, 3)] + "\t" + random.randint(1, 10).__str__() + '\n')
