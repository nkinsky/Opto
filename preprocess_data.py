## Script/functions to import openephys data and sync with other data

folder = r'C:\Users\Nat\Documents\UM\Working\Opto\Rat594\2019DEC06'

import OpenEphys as oe
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import glob
import pandas as pd


## Now load everything
# First import openephys data
cont_array = oe.loadFolder(folder)
events = oe.loadEvents(os.path.join(folder, 'all_channels.events'))

# Next import MATLAB data - must have only one mat file in folder!
mat_files = glob.glob('*.mat')
if len(mat_files) == 1:
    mat_data = sio.loadmat(os.path.join(folder, mat_files[0]))
else:
    mat_data = np.nan
    print('More than one .mat file in folder, unable to load')

# Import OptiTrack data here once you've exported it to a csv...
csv_files = glob.glob('*.csv')
if len(csv_files) == 1:
    opti_data = pd.read_csv(os.path.join(folder, csv_files[0]))
else:
    csv_data = np.nan
    print('More than one .csv file in folder, unable to load')

## Now plot stuff!!
