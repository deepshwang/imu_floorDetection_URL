# Floor Type Detection and Localization using IMU 
 This code is designed for specific types of data format
 Converts IMU csv data to kaggle format

## Background
This code is designed for specific types of data format. 
See more information [here](https://www.kaggle.com/jesucristo/1-smart-robots-most-complete-notebook/notebook)

## Input Data

### Where it came from

Input data is a csv file that is the product of conversion from rosbag file.

This conversion is done by [Atsushi Sakai](https://github.com/AtsushiSakai/rosbag_to_csv)

### Title of the input csv file

The file name must contain "wood", "terrazzo", or "tile" (private to URL)

## Output Data Structure

### seried_id

A group index consisting of 128 datum (1 measurement)


### measurement_number

Datum index within a single series.


### row_id      

A measurement uniquely expressed with series and measurement number.

### Contained information

orientation_X,Y,Z,W(quaternion) 

angular_velocity_X,Y,Z 

linear_acceleration_X,Y,Z


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


