# CSV to Kaggle form 
 This code is designed for specific types of data format
 Converts IMU csv data to kaggle format

## Background
This code is designed for specific types of data format

## Input Data

Input data is a csv file that is the product of conversion from rosbag file.

This conversion is done by [Atsushi Sakai](https://github.com/AtsushiSakai/rosbag_to_csv)

## Output Data

### Data structure
The data serves to train Convolutional Neural Network (CNN) with cross validation. 

In order to do so, the data are categorized into  "series_id", measurement_number", and "row_id".

*series_id:         A group index consisting of 128 datum (1 measurement)
measurement_number: Datum index within a single series.
row_id:             Unique row id expressed with series and measurement number.

### Contained information
The file contains information below (10 columns):
orientation_X,Y,Z,W(quaternion) / angular_velocity_X,Y,Z / linear_acceleration_X,Y,Z


## Prerequisites

### Python Modules

Using pip or anaconda, install appropriate Python modules

```
$conda install pandas
$conda install numpy
```

## How to use

1. Place the csv_to_kaggleform.py with the csv files to convert in the same folder.


2. Run the python code, and the formatted csv files will be saved in the same folder.


