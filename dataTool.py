import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from random import random

class imu_dataTool:
    def __init__(self):
        self.floortype_list=["wood", "tile", "terazzo"]
        self.data_class= self.wanted_data_class_selector()

    ###############################################
    #####   Methods for csv file Refinement   #####
    ###############################################


    def wanted_data_class_selector(self):
        i=0
        for data_class in os.listdir("raw_data"):
            print (data_class+ " : "+ str(i))
            i+=1
        data_class_select=int(raw_input("Type corresponding index you want to work with:  "))
        wanted_data_class=os.listdir("raw_data")[data_class_select]
        print ("You've selected: " + wanted_data_class)
        return wanted_data_class



    def csv_file_direction(self, data_type):
        csv_dir_list=[]
        root=os.getcwd()
        for path, subdirs, files in os.walk(root):
            for name in files:
                dir=os.path.join(path,name)
                dir_split=dir.split('/')
                if dir_split[-3]==data_type and dir_split[-2]==self.data_class and dir_split[-1][-4:] ==".csv":
                    csv_dir_list.append(dir)
        if data_type=='raw_data':
            self.raw_csv_dir_list=csv_dir_list
        elif data_type=='refined_data':
            self.refined_csv_dir_list=csv_dir_list
        return csv_dir_list


    ##### Main method #####
    def refine_csv(self):
        self.csv_file_direction("raw_data")
        df_list=[]
        for src_path in self.raw_csv_dir_list:
            df = pd.read_csv(src_path)
            df = df.drop(["time", ".header.seq", ".header.stamp.secs", ".header.stamp.nsecs", ".header.frame_id", ".orientation_covariance", ".angular_velocity_covariance", ".linear_acceleration_covariance"], axis=1)
            # df=df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'}, errors='raise')
            df = df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'})

            #df = df[df.angular_velocity_Z != 0]
            df.index = np.arange(0, len(df))
            df['measurement_number'] = df.index % 129
            df['series_id'] = df.index // 129
            df['row_id'] = df['series_id'].map(str) + "_" + df["measurement_number"].map(str)

            new_cols = ["row_id", "series_id", "measurement_number"] + df.columns.tolist()[:10]
            df = df[new_cols]
            df_list.append[df]

            save_path_split=src_path.split('/')
            save_path_split[-3]='refined_data'
            save_path_split[-1]='refined_'+save_path_split[-1]
            save_path='/'.join(save_path_split)
            save_folder='/'.join(save_path_split[:-1])
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            df.to_csv(save_path)
        print ("Refining COMPLETE")



    #########################################
    #####   Methods for Visualization   #####
    #########################################



    @staticmethod
    def csv_to_dataframe_in_list(target_files):
        pd_data_list = []
        for target_file_name in target_files:
            df = pd.read_csv(target_file_name)
            pd_data_list.append(df)
        return pd_data_list



    def ask_user_which_data_to_plot(self):
        self.csv_file_direction("refined_data")
        j=0
        for name in self.refined_csv_dir_list:
            print (name.split('/')[-1] + " : " + str(j))
            j+=1
        target_i=raw_input("Type index of data to draw. (Ex: 2, 3, 5 -> 235) : ")
        target_i_list=list(target_i)
        target_files=[]
        for k in target_i_list:
            target_files.append(self.refined_csv_dir_list[int(k)])
        return target_files



    def time_domain_plot(self, column_name):
        target_files=self.ask_user_which_data_to_plot()
        pd_data_list=self.csv_to_dataframe_in_list(target_files)
        for i, pd_data in enumerate(pd_data_list):
            datapoints = pd_data[column_name]
            plt.plot(range(datapoints.count()), datapoints, label=target_files[i].split('/')[-2:], linewidth=0.2)
        # plt.ylim(-0.1, 0.1)
        plt.rcParams["figure.figsize"] = (20, 15)
        plt.legend()
        plt.xlabel("Time stamp")
        plt.ylabel(column_name)
        fig = plt.gcf()
        root=os.getcwd()
        savedir=root+'/visualized_result/t_dom_plot_'+column_name+'.png'
        fig.savefig(savedir)
        plt.show()




    def freq_domain_plot_fft(self, column_name, initial_point=None, end_point=None):
        target_files=self.ask_user_which_data_to_plot()
        pd_data_list=self.csv_to_dataframe_in_list(target_files)
        for i, pd_data in enumerate(pd_data_list):
            datapoints=pd_data[column_name].to_numpy()
            if initial_point!=None and end_point!=None:
                datapoints=pd_data[column_name].to_numpy()[initial_point:end_point]
            fft_datapoints=abs(np.fft.fft(datapoints))[0:len(datapoints)]
            Fq=20  ### Sampling rate is 20Hz
            approx_freq_range=[x*Fq/float(len(datapoints)) for x in range(len(datapoints))]  # Reference: https://kr.mathworks.com/help/matlab/ref/fft.html
            half_length=len(approx_freq_range)//2
            plt.plot(approx_freq_range[0:half_length], fft_datapoints[0:half_length],  label=target_files[i].split('/')[-2:], linewidth=1)


        plt.legend()
        plt.xlabel("Frequnecy (Hz)")
        # plt.xlim(0, 2)
        plt.ylabel("Magnitude")
        title="Freq. range of <"+ column_name+">"
        plt.title(title)
        fig=plt.gcf()
        root=os.getcwd()
        savedir=root+'/visualized_result/f_dom_plot_fft_'+column_name+'.png'
        fig.savefig(savedir)
        plt.show()






if __name__=="__main__":
    imu_obj=imu_dataTool()
    imu_obj.freq_domain_plot_fft("angular_velocity_Z")
