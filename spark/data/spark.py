from __future__ import print_function
import itertools
from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
data = sc.textFile("/tmp/data/data_10000.txt", 2)  # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))  # tell each worker to split each line of it's partition
user_to_item = pairs.map(lambda pair: (pair[0], pair[1]))

# 2. Group data into (user_id, list of item ids they clicked on)
user_to_items = user_to_item.groupByKey()

# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_to_item_pairs = user_to_items.flatMapValues(lambda items: itertools.combinations(set(items), 2))

# 4. Transform into ((item1, item2), list of user1, user2 etc) where users
# are all the ones who co-clicked (item1, item2)
item_pair_to_user = user_to_item_pairs.map(lambda x: (x[1], x[0]))
item_pair_to_users = item_pair_to_user.groupByKey()

# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
item_pair_to_count = item_pair_to_users.map(lambda x: (x[0], len(x[1])))

# 6. Filter out any results where less than 3 users co-clicked the same pair of items
count = item_pair_to_count.filter(lambda x: x[1] >= 3)

output = count.collect()  # bring the data back to the master node so we can print it out
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
with open("output.txt", "w+") as output_file:
    for item_pair, count in output:
        print("{}\t{}\n".format(item_pair, count))
    print("Popular items done")
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

sc.stop()
