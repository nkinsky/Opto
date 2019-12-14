## Script/functions to import openephys data and sync with other data

# folder = r'C:\Users\Nat\Documents\UM\Working\Opto\Rat594\2019DEC06'
# folder ='/data/Working/Opto Project/Rat 594/Rat594_placestim2019-12-05_16-18-31/'
test_folder = '/data/Working/Opto Project/Place stim tests/Rat651_2019-12-10_08-54-56/'
test_bin_folder = '/data/Working/Opto Project/Rat 594/594_placestim_test_2019-12-04_10-24-25/experiment1/recording1/'

import Python3.OpenEphys as oe
import Python3.Binary as ob
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import glob
import pandas as pd
import helpers


## Now load everything
# First import openephys data
def load_openephys(folder):
    """Loads in openephys continuous and event data. Openephys format ok, binary format not yet finished/vetted"""
    try:  # Load in openephy format
        cont_array = oe.loadFolder(folder)
        events = oe.loadEvents(os.path.join(folder, 'all_channels.events'))
        oe_type = 'oe'
    except ZeroDivisionError:  # load in binary format - not yet finished

        binData, Rate = ob.Load(folder)
        SR = Rate['100']['0']  # get sample rate
        cont_time = np.load(os.path.join(folder, 'experiment1/recording1/continuous/Rhythm_FPGA-100.0/timestamps.npy'))
        event_folder = os.path.join(folder, 'experiment1/recording1/events/Rhythm_FPGA-100.0/TTL_1')
        event_data = []
        for file_name in ['channel_states.npy', 'channels.npy', 'full_words.npy', 'timestamps.npy']:
            event_data.append(np.load(os.path.join(event_folder, file_name)))
        oe_type = 'binary'

    return event_data, cont_array


## Next import MATLAB data - must have only one mat file in folder!
def load_mat(folder):
    """
    Load .mat file with synchornized optitrack time/position, linear position, matlab time, trigger events, and start/minute
    tracker
    :param:
    """
    mat_files = glob.glob(os.path.join(folder, '*.mat'))
    if len(mat_files) == 1:
        mat_data = sio.loadmat(os.path.join(folder, mat_files[0]))
    elif len(mat_files) == 0:
        mat_data = np.nan
        print('No .mat files in folder, unable to load')
    else:
        mat_data = np.nan
        print('No More than one .mat file in folder, unable to load')

    return mat_data


## Import OptiTrack data here once you've exported it to a csv...
def load_opti(folder):
    """
    Loads optitrack CSV folder - needs a check to make sure you are always loading the position and not rotation values.
    Also needs to get start time/hour for later interpolation!!!
    """
    csv_files = glob.glob(os.path.join(folder, '*.csv'))
    if len(csv_files) == 1:
        opti_data = pd.read_csv(os.path.join(folder, csv_files[0]), header=5)
        temp = pd.read_csv(os.path.join(folder, csv_files[0]), header=0)
        opti_start_time = temp.keys()[3][-11:-3]
    elif len(csv_files) == 0:
        opti_data = np.nan
        print('No .csv files in folder, unable to load')
    else:
        opti_data = np.nan
        print('More than one .csv file in folder, unable to load')

    return opti_data, opti_start_time


## Now plot stuff
#
# # get time of MATLAB TTL pulse out!!!
# oe_zero = event_data[3][event_data[0] == 8]/SR
# start_hour = 16  # from .csv output file, hour (24-hr format) that data starts recording in - figure this out!!!!


## Plot x,y,z, pos over time
def plot_opti_v_mat(opti_data, mat_data):
    fig1, ax1 = plt.subplots(3, 2)
    fig1.set_size_inches([10, 6.4])
    ax1[0][0].plot(opti_data['Time (Seconds)'], opti_data['X.2'])
    ax1[1][0].plot(opti_data['Time (Seconds)'], opti_data['Y.2'])
    ax1[2][0].plot(opti_data['Time (Seconds)'], opti_data['Z.2'])

    # Get time elapsed
    tdiff = helpers.mat_time_to_sec(mat_data['time_mat'][0, :], mat_data['time_mat'])

    ax1[0][1].plot(tdiff,  mat_data['pos_opti'][:, 0])
    ax1[1][1].plot(tdiff, mat_data['pos_opti'][:, 1])
    ax1[2][1].plot(tdiff, mat_data['pos_opti'][:, 2])

    # plot x/z overhead...
    fig2, ax2 = plt.subplots(1, 2)
    fig2.set_size_inches([6.4, 4.8])
    ax2[0].plot(opti_data['X.2'], opti_data['Z.2'])
    ax2[0].set_title('Optitrack')
    ax2[1].plot(mat_data['pos_opti'][:,0], mat_data['pos_opti'][:,2])
    ax2[1].set_title('Opti API -> MATLAB')

    return fig1, ax1, fig2, ax2


# Get start time


## Now plot stuff!!

if __name__ == '__main__':
    mat_data = load_mat(test_folder)
    opti_data, opti_start_time = load_opti(test_folder)
    plot_opti_v_mat(opti_data, mat_data)

    pass