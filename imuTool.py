import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from random import random
from random import shuffle

class imu_dataTool:
    def __init__(self):
        self.floortype_list = ["wood", "tile", "terazzo"]
        self.list_data_class_to_refine = self.to_refine_data_class_selector()

    ###############################################
    #####   Methods for csv file Refinement   #####
    ###############################################


    def to_refine_data_class_selector(self):
        raw_data_classlist = os.listdir('raw_data')
        refined_data_classlist = os.listdir('refined_data')
        list_data_class_to_refine = [i for i in raw_data_classlist if not i in refined_data_classlist]
        return list_data_class_to_refine



    def to_refine_csv_file_direction(self, data_type, data_class_list): #data_type :'raw_data' or 'refined_data' /// data_class : 'kobuki_sample' or 'xsens_nov_5'....
        csv_dir_list = []
        root = os.getcwd()
        for data_class in data_class_list:
            for path, subdirs, files in os.walk(root):
                for name in files:
                    dir = os.path.join(path,name)
                    dir_split = dir.split('/')
                    if dir_split[-3] == data_type and dir_split[-2] == data_class and dir_split[-1][-4:] == '.csv':
                        csv_dir_list.append(dir)
        return csv_dir_list


    ####   MAIN METHID   ####
    # Refines whatever raw_data files there are that haven't been refined.
    def refine_csv(self):
        path_lists = self.to_refine_csv_file_direction('raw_data', self.list_data_class_to_refine)
        df_list = []
        for src_path in path_lists:
            df = pd.read_csv(src_path, index_col=False)
            df = df.drop(["time", ".header.seq", ".header.stamp.secs", ".header.stamp.nsecs", ".header.frame_id", ".orientation_covariance", ".angular_velocity_covariance", ".linear_acceleration_covariance"], axis=1)
            # df=df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'}, errors='raise')
            df = df.rename(columns = {'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'})

            #df = df[df.angular_velocity_Z != 0]
            df.index = np.arange(0, len(df))
            df_list.append(df)

            save_path_split = src_path.split('/')
            save_path_split[-3] = 'refined_data'
            save_path_split[-1] = 'refined_'+save_path_split[-1]
            save_path = '/'.join(save_path_split)
            save_folder = '/'.join(save_path_split[:-1])
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            df.to_csv(save_path)
        print ("Refining COMPLETE")



    #########################################
    #####   Methods for Visualization   #####
    #########################################



    @staticmethod
    def csv_to_dataframe_in_list(target_files):
        root = os.getcwd()
        pd_data_list = []
        for target_file_name in target_files:
            dir=os.path.join(root,target_file_name)
            df = pd.read_csv(dir)
            pd_data_list.append(df)
        return pd_data_list



    def time_domain_plot(self, column_name, target_files):
        pd_data_list = self.csv_to_dataframe_in_list(target_files)
        for i, pd_data in enumerate(pd_data_list):
            datapoints = pd_data[column_name]
            plt.plot(range(datapoints.count()), datapoints, label=target_files[i].split('/')[-2:], linewidth=0.2)
        # plt.ylim(-0.1, 0.1)
        plt.rcParams["figure.figsize"] = (20, 15)
        plt.legend()
        plt.xlabel("Time stamp")
        plt.ylabel(column_name)
        fig = plt.gcf()
        root = os.getcwd()
        savedir = root+'/visualized_result/t_dom_plot_'+column_name+'.png'
        fig.savefig(savedir)
        plt.show()



    def freq_domain_plot_fft(self,column_name,target_files, initial_point=None, end_point=None):
        pd_data_list = self.csv_to_dataframe_in_list(target_files)
        for i, pd_data in enumerate(pd_data_list):
            datapoints = pd_data[column_name].to_numpy()
            if initial_point!=None and end_point!=None:
                datapoints = pd_data[column_name].to_numpy()[initial_point:end_point]
            fft_datapoints = abs(np.fft.fft(datapoints))[0:len(datapoints)]
            Fq = 20  ### Sampling rate is 20Hz
            approx_freq_range = [x*Fq/float(len(datapoints)) for x in range(len(datapoints))]  # Reference: https://kr.mathworks.com/help/matlab/ref/fft.html
            half_length = len(approx_freq_range)//2
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



    ##################################################################
    #####   Methods for Neural Network Training Data Formation   #####
    ##################################################################



    def NN_train_data_creator(self, target_files):
        pd_data_list = self.csv_to_dataframe_in_list(target_files)

        #Tag answers
        for i in range(len(target_files)):
            df=pd_data_list[i]
            surface=target_files[i].split('/')[-1].split('_')[1]
            if surface=='wood':
                g_id=2
            elif surface=='tile':
                g_id=1
            elif surface=='terazzo':
                g_id=0
            df['group_id'] = g_id
            df['surface'] = surface
            new_cols = ['group_id', 'surface'] + df.columns.tolist()[:10]
            df = df[new_cols]

            ## Drop remainders
            df.drop(df.tail(df.shape[0]%128).index,inplace=True)
            pd_data_list[i]=df

        # Combine the truncated dfs
        df_concat=pd.concat(pd_data_list, ignore_index=True)

        # Divide dfs by sets of 128 measurements
        df_p_list=[]
        for i in range (int(df_concat.shape[0]//128)):
            if i<int(df_concat.shape[0]//128)-1:
                df_p=df_concat.loc[i*128:128*(i+1)-1]
                df_p_list.append(df_p)

        # Shuffle for fair training sequence
        shuffle(df_p_list)

        # Label series_id and measurement number
        df = pd.concat(df_p_list, ignore_index=True)
        df.index = np.arange(0, len(df))
        df['measurement_number'] = df.index % 128
        df['series_id'] = df.index // 128
        df['row_id'] = df['series_id'].map(str) + "_" + df["measurement_number"].map(str)
        new_cols = ['group_id','surface','row_id', 'series_id', 'measurement_number'] + df.columns.tolist()[2:12]
        df = df[new_cols]

        # Extract trainX
        df_X=df[df.columns.tolist()[2:]]

        #Extract trainY
        df_Y=df.loc[df['measurement_number'].isin([0])][['series_id','group_id', 'surface']]

        #Export to csv
        df_X.to_csv("NN_train_data/X_train.csv", index=False)
        df_Y.to_csv("NN_train_data/y_train.csv", index=False)









if __name__=="__main__":
    target_files = ["refined_data/xsens_nov_5/refined_terazzo_2.csv",
                    "refined_data/xsens_nov_5/refined_tile_2.csv",
                    "refined_data/xsens_nov_5/refined_wood_2.csv"]


    imu_obj=imu_dataTool()
    imu_obj.refine_csv()
    imu_obj.NN_train_data_creator(target_files)
