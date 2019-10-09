import matplotlib.pyplot as plt
import pandas as pd
from random import random

COLORSET = [(241/255.0, 101/255.0, 65/255.0), (2/255.0, 23/255.0, 157/255.0), (19/255.0, 128/255.0, 20/255.0), (191/255.0, 17/255.0, 46/255.0)]
LINE = ['--', '-.', ':', '-.', '-.']
LABEL = ["terazzo", "tile", "wood"]


if __name__ == "__main__":
    target_files = ["refined_result/refined_terazzo_2.csv",
                    "refined_result/refined_tile_2.csv",
                    "refined_result/refined_wood_2.csv"]

    pd_data_list = []
    for target_file_name in target_files:
        df = pd.read_csv(target_file_name)
        pd_data_list.append(df)

    for i, pd_data in enumerate(pd_data_list):
        vel_z = pd_data['angular_velocity_Z']
        plt.plot(range(vel_z.count()), vel_z, label=LABEL[i])

    plt.ylim(-0.1, 0.1)
    plt.legend()
    plt.xlabel("Time stamp")
    plt.ylabel("vel_z")
    fig = plt.gcf()
    plt.show()
    fig.savefig("data_comparison.png")
