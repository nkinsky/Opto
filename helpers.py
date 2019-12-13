# helper functions
import numpy as np
import datetime

def mat_time_to_sec(t0, t):

    # Get start time
    year0 = int(t0[0])
    month0 = int(t0[1])
    day0 = int(t0[2])
    hour0 = int(t0[3])
    min0 = int(t0[4])
    sec0 = int(np.floor(t0[5]))
    msec0 = int((t0[5]-sec0)*1000000)
    t0py = datetime.datetime(year0, month0, day0, hour0, min0, sec0, msec0)

    # Get times to compare
    year = int(t[:, 0])
    month = int(t[:, 1])
    day = int(t[:, 2])
    hour = int(t[:, 3])
    min = int(t[:, 4])
    sec = int(np.floor(t[:, 5]))
    msec = int((t[:, 5] - sec)*1000000)

    tdiff = []
    for yr, mo, dy, hr, mi, s, ms in zip(year, month, day, hour, min, sec, msec):
        diff_temp = t0py - datetime.datetime(yr, mo, dy, hr, mi, s, ms)
        tdiff.append(diff_temp.total_seconds())

    return tdiff


