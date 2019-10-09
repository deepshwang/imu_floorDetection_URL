import pandas as pd
import numpy as np
import os
import time

CLASS_LIST = ["wood", 'tile', 'terazzo']


def get_raw_csv_list(dir):
    candidates = os.listdir(dir)
    target_csv_list = []
    for name in candidates:
        if name[:4] in CLASS_LIST or name[:7] in CLASS_LIST:
            csv_path = os.path.join(dir, name)
            target_csv_list.append(csv_path)
    return target_csv_list


def refine_csv(src_path):
    df = pd.read_csv(src_path)
    df = df.drop(["time", ".header.seq", ".header.stamp.secs", ".header.stamp.nsecs", ".header.frame_id", ".orientation_covariance", ".angular_velocity_covariance", ".linear_acceleration_covariance"], axis=1)
    # df=df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'}, errors='raise')
    df = df.rename(columns={'.orientation.x': 'orientation_X', '.orientation.y': 'orientation_Y', '.orientation.z': 'orientation_Z', '.orientation.w': 'orientation_W', '.angular_velocity.x': 'angular_velocity_X', '.angular_velocity.y': 'angular_velocity_Y', '.angular_velocity.z': 'angular_velocity_Z', '.linear_acceleration.x': 'linear_acceleration_X', '.linear_acceleration.y': 'linear_acceleration_Y', '.linear_acceleration.z': 'linear_acceleration_Z'})

    df = df[df.angular_velocity_Z != 0]
    df.index = np.arange(0, len(df))
    df['measurement_number'] = df.index % 129
    df['series_id'] = df.index // 129
    df['row_id'] = df['series_id'].map(str) + "_" + df["measurement_number"].map(str)

    new_cols = ["row_id", "series_id", "measurement_number"] + df.columns.tolist()[:10]
    df = df[new_cols]
    if not "/" in src_path:
        df.to_csv("refined" + src_path)
    else:
        src_name = src_path.split("/")[-1]
        df.to_csv("refined" + src_name)


if __name__ == "__main__":
    target_dir = "raw_data"
    csv_list = get_raw_csv_list(target_dir)
    print(csv_list)

    for csv_path in csv_list:
        refine_csv(csv_path)
    print("Refining COMPLETE!")
