import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import random


COLORSET = [(241/255.0, 101/255.0, 65/255.0), (2/255.0, 23/255.0, 157/255.0), (19/255.0, 128/255.0, 20/255.0), (191/255.0, 17/255.0, 46/255.0)]
LINE = ['--', '-.', ':', '-.', '-.']
LABEL = ["terazzo", "tile", "wood"]

def csv_to_dataframe_in_list(target_files):
    pd_data_list = []
    for target_file_name in target_files:
        df = pd.read_csv(target_file_name)
        pd_data_list.append(df)
    return pd_data_list


def plot_dataframe_for_columns(column_name, pd_data_list):
    for i, pd_data in enumerate(pd_data_list):
        datapoints = pd_data[column_name]
        plt.plot(range(datapoints.count()), datapoints, label=LABEL[i])

    plt.ylim(-0.1, 0.1)
    plt.legend()
    plt.xlabel("Time stamp")
    plt.ylabel("vel_z")
    fig = plt.gcf()
    plt.show()
    fig.savefig("data_comparison.png")

def plot_fft_for_columns(column_name, pd_data_list):
    for i, pd_data in enumerate(pd_data_list):
        datapoints=pd_data[column_name].to_numpy()
        fft_datapoints=abs(np.fft.fft(datapoints))[0:len(datapoints)]
        Fq=20  ### Sampling rate is 20Hz
        approx_freq_range=[x*Fq/len(datapoints) for x in range(len(datapoints))]  # Reference: https://kr.mathworks.com/help/matlab/ref/fft.html
        half_length=len(approx_freq_range)//2
        plt.plot(approx_freq_range[0:half_length], fft_datapoints[0:half_length], label=LABEL[i])


    plt.legend()
    plt.xlabel("Frequnecy (Hz)")
    plt.ylabel("Magnitude")
    title="Freq. range of <"+ column_name+">"
    plt.title(title)
    fig=plt.gcf()
    filename="DFT_freq_range_"+column_name+".png"
    fig.savefig(filename)
    plt.show()




#################    MAIN OPERATION    ##################


if __name__ == "__main__":
    target_files = ["refined_result/refined_terazzo_2.csv",
                    "refined_result/refined_tile_2.csv",
                    "refined_result/refined_wood_2.csv"]

    pd_data_list=csv_to_dataframe_in_list(target_files)

    #plot_dataframe_for_column('angular_velocity_Z', pd_data_list)
    plot_fft_for_columns('angular_velocity_Z',pd_data_list)
