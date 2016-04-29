import random
with open('names.txt') as input_file:
    with open("data.txt","w+") as output_file:
        # compile list of names from input_file
        names = []
        for line in input_file:
            items = line.split(" ")

            names.append(items[0])

        # assign random names a random product id
        for i in range(10000):
            output_file.write(names[random.randint(0, names.__len__()-1)] + "\t" + random.randint(1, 100).__str__() + '\n')
