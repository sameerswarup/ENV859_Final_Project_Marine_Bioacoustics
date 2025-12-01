#%% Import Libraries
import numpy as np
import os
import pandas as pd
import glob
from scipy.io import loadmat
os.chdir("C:\\Users\\ghg7\\Desktop\\MP Data\\Focal Whale Call Data w GPS")

#%% Import Date/Time Data

df = pd.read_csv(
    "Focal Calls\\bp23_205c_selections_datetime.txt",
    sep="\t",          # tab-delimited
    engine="python",   # handles irregular fields safely
)

print(df.shape)
print(df.head())

#%% Import Focal Call Data

df = pd.read_csv(
    "Focal Calls\\bp23_205c_selections_focal.txt",
    sep="\t",          # tab-delimited
    engine="python",   # handles irregular fields safely
)

print(df.shape)
print(df.head())

# %% Aggregate All Focal Call Data

dfs = []

for file in glob.glob("C:\\Users\\ghg7\\Desktop\\MP Data\\Focal Whale Call Data w GPS\\Focal Calls\\*.txt"):
    print("Reading:", file)

    df = pd.read_csv(
        file,
        sep="\t",
        engine="python"
    )

    # enforce 24 columns
    df = df.iloc[:, :24]
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

print(combined.shape)

dfs

# %%Getting GPS coordinates from Matlab

mat_data = loadmat('finGPS\\bp23_205c\\bp23_205c001gps.mat')
print(mat_data.keys())  # shows variable names inside the .mat file


# %% Printing variables to look at data (edit to produce coordinates)
myvar = mat_data['obs'] #prints empty list, troubleshoot

#print(myvar)
# %%
pd.DataFrame(myvar[0])

# %%
