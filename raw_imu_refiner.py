import pandas as pd
import numpy as np
import os
import time

class imu_refine:
    def __init__(self):
        self.floortype_list=["wood", "tile", "terazzo"]
        self.data_class= self.wanted_data_class_selector()
        self.raw_csv_dir_list= self.get_csv_file_direction()



    def wanted_data_class_selector(self):
        i=0
        for data_class in os.listdir("raw_data"):
            print (data_class+ " : "+ str(i))
            i+=1
        data_class_select=int(raw_input("Type corresponding index you want to refine."))
        wanted_data_class=os.listdir("raw_data")[data_class_select]
        print ("You've selected: " + wanted_data_class)
        return wanted_data_class



    def get_csv_file_direction(self):
        raw_csv_dir_list=[]
        root=os.getcwd()
        for path, subdirs, files in os.walk(root):
            for name in files:
                dir=os.path.join(path,name)
                dir_split=dir.split('/')
                if dir_split[-3]=='raw_data' and dir_split[-2]==self.data_class and dir_split[-1][-4:] ==".csv":
                    raw_csv_dir_list.append(dir)
        return raw_csv_dir_list



    def refine_csv(self):
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

            save_path_split=src_path.split('/')
            save_path_split[-3]='refined_result'
            save_path_split[-1]='refined_'+save_path_split[-1]
            save_path='/'.join(save_path_split)
            save_folder='/'.join(save_path_split[:-1])
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            df.to_csv(save_path)

if __name__=="__main__":
    refine_obj=imu_refine()
    refine_obj.refine_csv()
