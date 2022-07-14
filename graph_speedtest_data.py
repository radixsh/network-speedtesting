import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import datetime as dt

# https://pynative.com/python-list-files-in-a-directory/
# Get a list of all the files in the subdirectory containing my speedtest data
datafiles = os.listdir('data')

# Will be populated like: info['router 2.4GHz'] = [14.94, 19.68]
info = {}
# As we go through the datafiles, we will make note of each timestamp on them,
# and we will eventually find the timespan over which the data was taken
dates = []

for filename in datafiles:
    f = open(f"data/{filename}", "r")
    # The first line is like "router 2.4GHz (2022-07-13_19-07)"
    header = f.readline().rstrip()
    name = ' '.join(header.split()[:2])

    # Save the date (stripped of its parentheses) to an array. We'll calculate
    # the spread of the data once we've got all the dates.
    date = header.split()[2][1:-1]
    date = dt.datetime.strptime(date, '%Y-%m-%d_%H-%M')
    dates.append(date)

    # Lines 2, 4, etc hold download info, and lines 3, 5, etc hold upload info.
    # Set a flag to mark the even-number lines as "download data".
    is_download = True
    dl = [] # Will hold data from lines 2, 4, etc
    ul = [] # Will hold data from lines 3, 5, etc
    # Extract the floats from each line, and sort using the is_download flag
    for line in f:
        # If any speedtests failed, they produce empty lines rather than lines
        # like "Download: 31.41 Mbps" and "Upload: 59.26 Mbps". However, Python
        # will silently cast a blank line to the float 0.0. We must ignore empty
        # lines.
        # https://stackoverflow.com/questions/7896495/python-how-to-check-if-a-line-is-an-empty-line
        if not line.strip():
            pass
        for word in line.split():
            try:
                if is_download:
                    dl.append(float(word))
                else:
                    ul.append(float(word))
            except:  # If the word is not a float
                pass
        # Toggle the flag
        is_download = not is_download

    # Append the average download/upload speeds from this one file to the
    # running dict of download/upload speeds (this one file only analyzes one
    # network, so it contributes only two data points total: one for download,
    # one for upload)
    info[f"{name}\n{date.strftime('%b %d (%H:%M)')}"] = [np.mean(dl), np.mean(ul)]

print(f'Analyzed: {str(info.keys())}')

# https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
# fig = plt.figure()

fig, ax = plt.subplots(figsize=(20,20))

plt.legend(["Download", "Upload"], loc=2)
plt.ylabel("Network speed (Mbps)")

'''
# Find the spread of the dates, and use this to title the figure
# https://stackabuse.com/converting-strings-to-datetime-in-python/
python_readable_datetimes = []
for d in dates:
    d = d[1:]
    d = d[:-1]
    python_readable_datetimes.append(dt.datetime.strptime(d, '%Y-%m-%d_%H-%M'))
'''
spread = max(dates) - min(dates)
# timedelta stores seconds, so get minutes like this
spread = int(spread.seconds / 60)
plt.title(f"Network performance (spanning {spread} minutes)")

## # Evenly space out the downloads bars
## WIDTH = 0.1
## x = np.arange(len(info))
## downloads_bar = x - WIDTH
## # The uploads bar will be offset to the right of the downloads bar, resulting in
## # the downloads/uploads bars for each network being grouped together
## uploads_bar = x + WIDTH

# Pull the list values of the dict out into their own lists, one by one (ugly,
# but Python complained at me when I tried to directly read info.values()[0])
downloads = []
uploads = []
# The dict is formatted like info['router 2.4GHz'] = [13.94, 19.68]
for conn in info.values():
    downloads.append(conn[0])
    uploads.append(conn[1])

# plt.bar(downloads_bar, downloads, color="green", width=WIDTH)
# plt.bar(uploads_bar, uploads, color="blue", width=WIDTH)

# TODO: make the double bars closer together lol
WIDTH = 0.01
x_axis = np.arange(len(info))  # [i*2 for i in range(len(info))]
print("x_axis: " + str(x_axis))
# By editing the x_axis between the x-values, you change the space between bars
# dlbar = [i - WIDTH for i in x_axis]
# print("dlbar: " + str(dlbar))
# ulbar = [i + WIDTH for i in x_axis]
# print("ulbar: " + str(ulbar))
plt.bar(x_axis - WIDTH, downloads, color="green", width=WIDTH*2)
plt.bar(x_axis + WIDTH, uploads, color="blue", width=WIDTH*2)

# The first parameter is the same as above, but the second parameter is the
# actual text to display
plt.xticks(x_axis, info.keys())
for tick in ax.get_xticklabels():
        tick.set_rotation(90)

plt.savefig("results")
