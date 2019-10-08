import pandas as pd
import numpy as np
import os
import time

def name_collector():
    path=os.getcwd()
    filedir=os.listdir(path)
    finaldir=[]
    for name in filedir:
        if name[:4]=="wood" or name[:4]=="tile" or name[:7]=="terazzo":
            finaldir.append(name)
    return finaldir


def refiner(finaldir):
    for name in finaldir:
        df=pd.read_csv(name)
        df=df.drop(["time",".header.seq", ".header.stamp.secs", ".header.stamp.nsecs", ".header.frame_id", ".orientation_covariance", ".angular_velocity_covariance", ".linear_acceleration_covariance"], axis=1)
        df=df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'}, errors='raise')


        df = df[df.angular_velocity_Z != 0]
        df.index = np.arange(0, len(df))
        df['measurement_number']=df.index%129
        df['series_id']=df.index//129
        df['row_id']=df['series_id'].map(str)+"_"+df["measurement_number"].map(str)

        new_cols=["row_id", "series_id", "measurement_number"]+df.columns.tolist()[:10]
        df=df[new_cols]

        df.to_csv("refined_"+name)

##Function Operation
refiner(name_collector())
print ("Refining COMPLETE!")
