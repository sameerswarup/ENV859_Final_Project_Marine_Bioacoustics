#%% Import Libraries
import numpy as np
import os
import pandas as pd
import glob
import arcpy
import csv
#os.chdir("V:\\MP Data\\Focal Whale Call Data w GPS")
os.chdir(r"/Users/sameerswarup/Documents/Duke MEM Classes/Fall 2025/Advanced_GIS/ENV859_Final_Project_Marine_Bioacoustics/Data")

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

#%% Create ArcGIS point objects out of entries in Filtered_Parents.csv

filtered_parents_csv_path = r"/Users/sameerswarup/Documents/Duke MEM Classes/Fall 2025/Advanced_GIS/ENV859_Final_Project_Marine_Bioacoustics/Data/Filtered_Parents.csv"
out_path = r"/Users/sameerswarup/Documents/Duke MEM Classes/Fall 2025/Advanced_GIS/ENV859_Final_Project_Marine_Bioacoustics/Data/"
out_fc = r"Filtered_Parents_Points"
source_id_field = "Tag"  # Column in CSV to use as ID

# Create a point feature class with WGS84 coordinates from entries in Filtered_Parents
arcpy.management.XYTableToPoint(
    in_table=filtered_parents_csv_path,
    out_feature_class=f"{out_path}\\{out_fc}",
    x_field="Longitude",
    y_field="Latitude",
    coordinate_system=arcpy.SpatialReference(4326)  # WGS84
)

# Add ID field
arcpy.management.AddField(f"{out_path}\\{out_fc}", "ID", "LONG")

# Copy values from CSV column to ID field
with arcpy.da.UpdateCursor(f"{out_path}\\{out_fc}", ["ID"]) as cursor, \
     open(filtered_parents_csv_path, "r") as f:
    
    reader = csv.DictReader(f)
    rows = list(reader)
    
    for i, row in enumerate(cursor):
        # Assign the ID from CSV (assumes order matches XYTableToPoint)
        cursor.updateRow([int(rows[i][source_id_field])])
