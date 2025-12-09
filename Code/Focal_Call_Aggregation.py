#%% Import Libraries
import numpy as np
import os
import pandas as pd
import glob
os.chdir("V:\\MP Data\\Focal Whale Call Data w GPS")

#%% Import Parent .csv files with Call and Coordinate Data integrated from single files

#import Parent Call List and Parent Coordinates
parent_calls = pd.read_csv("Parent_Call_List.csv")
parent_coords = pd.read_csv("Parent_Coordinates.csv")

# Merge Parent Call List with Parent Coordinates on "Tag" column
merged_data = pd.merge(parent_calls, parent_coords, on="Tag", how="inner")

# Export merged files to CSV
merged_data.to_csv("Merged_Parents.csv", index=False)

# %% Filter for Results with Similar Times

# Merged csvs bring in two time columns, "time_x" from Parent Call List and "time_y" from Parent Coordinates
# Convert time columns to datetime objects
merged_data["Time_x"] = pd.to_datetime(merged_data["Time_x"])
merged_data["Time_y"] = pd.to_datetime(merged_data["Time_y"])

# Calculate absolute time difference between the two time columns
merged_data["time_diff"] = (merged_data["Time_x"] - merged_data["Time_y"]).abs()

filtered_data = merged_data[merged_data["time_diff"] <= pd.Timedelta(minutes=90)]

# Export filtered results to CSV
filtered_data.to_csv("Filtered_Parents.csv", index=False)
