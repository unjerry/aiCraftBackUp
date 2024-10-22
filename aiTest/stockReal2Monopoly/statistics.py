import json
from datetime import datetime
import matplotlib.pyplot as plt

name = input("name:")

with open("data/{:s}.json".format(name), "r") as file:
    data = json.load(file)

print(data["column"])
item_list = data["item"]

for i in range(10):
    # print(item_list[i])
    print(datetime.fromtimestamp(int(item_list[i][0] / 1000)))

time_X = [datetime.fromtimestamp(item[0] / 1000) for item in item_list]
value_Y = [item[5] for item in item_list]

print(time_X[:10])
print(value_Y[:10])

fig = plt.figure(figsize=(100, 5), dpi=300)
plt.scatter(time_X, value_Y)
plt.grid()
fig.savefig("fig/close_of_{:s}.png".format(name))

fig = plt.figure(dpi=300)
plt.hist(
    value_Y[
        int(len(value_Y) / 2)
        + int(len(value_Y) / 4)
        + 0 : int(len(value_Y) / 2)
        + int(len(value_Y) / 4)
        + int(len(value_Y) / 4)
    ],
    bins=20,
)
plt.grid()
fig.savefig("fig/hist_of_{:s}.png".format(name))

fig = plt.figure(dpi=500)
plt.boxplot(
    [
        value_Y[0 : int(len(value_Y))],
        value_Y[0 : int(len(value_Y) / 2)],
        value_Y[
            int(len(value_Y) / 2) + 0 : int(len(value_Y) / 2) + int(len(value_Y) / 2)
        ],
        value_Y[0 : int(len(value_Y) / 4)],
        value_Y[
            int(len(value_Y) / 4) + 0 : int(len(value_Y) / 4) + int(len(value_Y) / 4)
        ],
        value_Y[
            int(len(value_Y) / 2) + 0 : int(len(value_Y) / 2) + int(len(value_Y) / 4)
        ],
        value_Y[
            int(len(value_Y) / 2)
            + int(len(value_Y) / 4)
            + 0 : int(len(value_Y) / 2)
            + int(len(value_Y) / 4)
            + int(len(value_Y) / 4)
        ],
    ]
)
plt.grid()
fig.savefig("fig/boxplot_of_{:s}.png".format(name))

fig = plt.figure(dpi=500)
plt.boxplot(
    [
        value_Y[int(len(value_Y)) - int(len(value_Y) / 1) : int(len(value_Y))],
        value_Y[int(len(value_Y)) - int(len(value_Y) / 2) : int(len(value_Y))],
        value_Y[int(len(value_Y)) - int(len(value_Y) / 4) : int(len(value_Y))],
        value_Y[int(len(value_Y)) - int(len(value_Y) / 8) : int(len(value_Y))],
        value_Y[int(len(value_Y)) - int(len(value_Y) / 16) : int(len(value_Y))],
    ]
)
plt.xticks(
    [
        1,
        2,
        3,
        4,
        5,
    ],
    [
        "{:d}-{:.2f}".format(int(len(value_Y) / 1), int(len(value_Y) / 1) / 242),
        "{:d}-{:.2f}".format(int(len(value_Y) / 2), int(len(value_Y) / 2) / 242),
        "{:d}-{:.2f}".format(int(len(value_Y) / 4), int(len(value_Y) / 4) / 242),
        "{:d}-{:.2f}".format(int(len(value_Y) / 8), int(len(value_Y) / 8) / 242),
        "{:d}-{:.2f}".format(int(len(value_Y) / 16), int(len(value_Y) / 16) / 242),
    ],
)
plt.grid()
fig.savefig("fig/expboxplot_of_{:s}.png".format(name))
