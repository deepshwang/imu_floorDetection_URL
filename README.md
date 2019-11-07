# Floor Type Detection and Localization using IMU 
 Workspace to deal IMU data for floor type detection and localization

## Background
This code is designed for specific types of data format. 
See more information [here](https://www.kaggle.com/jesucristo/1-smart-robots-most-complete-notebook/notebook)

## imuTool.py

### csv_refine(target_files)

- Converts target files in raw_data folder and saves refined data in refined_data folder

- Automatically select and convert raw datas that hasn't been converted

### time_domain_plot(column_name, target_files)

- Plots files in target_files (list of directions) for columns in "column_name"

### freq_domain_plot_fft(self,column_name,target_files, initial_point=None,end_point=None)

- Draws spatial domain plot in target_files (list of directions )for columns in "column_name"

- Can optionally set 'initial_point' and 'end_point' (integers), which sets domain for the plot.


## Information on data

### rosbag -> csv

This conversion is done by [Atsushi Sakai](https://github.com/AtsushiSakai/rosbag_to_csv)

### Contained information

orientation_X,Y,Z,W(quaternion) 

angular_velocity_X,Y,Z 

linear_acceleration_X,Y,Z

