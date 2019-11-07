from imuTool import imu_dataTool

###   Parameters   ###
target_files = ["refined_data/xsens_nov_5/refined_terazzo_2.csv",
                "refined_data/xsens_nov_5/refined_tile_2.csv",
                "refined_data/xsens_nov_5/refined_wood_2.csv"]

column_name='angular_velocity_Z'



###   Operation   ###
imu_obj=imu_dataTool()

imu_obj.time_domain_plot(column_name, target_files)
