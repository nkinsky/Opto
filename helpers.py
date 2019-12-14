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
    year = t[:, 0]
    month = t[:, 1]
    day = t[:, 2]
    hour = t[:, 3]
    min = t[:, 4]
    sec = np.floor(t[:, 5])
    msec = (t[:, 5] - sec)*1000000

    tdiff = []
    for yr, mo, dy, hr, mi, s, ms in zip(year, month, day, hour, min, sec, msec):
        diff_temp = datetime.datetime(int(yr), int(mo), int(dy), int(hr), int(mi), int(s), int(ms)) - t0py
        tdiff.append(diff_temp.total_seconds())

    return tdiff


if __name__ == '__main__':


    pass