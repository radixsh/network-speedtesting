import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# https://pynative.com/python-list-files-in-a-directory/
# Get a list of all the files in the subdirectory containing my speedtest data
datafiles = os.listdir('data')

network_names = []
all_download_speeds = []
all_upload_speeds = []

for filename in datafiles:
    f = open(f"data/{filename}", "r")
    # The first line names the network being tested:
    header = f.readline().rstrip()
    network_names.append(header)
    # Lines 2, 4, etc hold download info, and lines 3, 5, etc hold upload info.
    # Set a flag to mark the even-number lines as "download data".
    is_download = True 
    dl = [] # Will hold data from lines 2, 4, etc
    ul = [] # Will hold data from lines 3, 5, etc
    # Extract the floats from each line, and sort using the is_download flag
    for line in f:
        # If any speedtests failed, they produce empty lines rather than lines
        # like "Download: 31.41 Mbps" and "Upload: 59.26 Mbps". However, Python
        # will successfully cast a blank line to the float 0.0. We must ignore
        # empty lines. 
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
    # running list of download/upload speeds (this one file only analyzes one
    # network, so it contributes only two data points total: one for download,
    # one for upload)
    all_download_speeds.append(np.mean(dl))
    all_upload_speeds.append(np.mean(ul))

print(f'Analyzed: {network_names}')

# https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
fig = plt.figure()
WIDTH = 0.25

# Evenly space out the downloads bars
downloads = np.arange(len(all_download_speeds)) + WIDTH
# The uploads bar will be just to the right of the downloads bar, resulting in
# the downloads/uploads bars for each network being grouped together
uploads = [x + WIDTH for x in downloads]

plt.bar(downloads, all_download_speeds, color="green", width=WIDTH)
plt.bar(uploads, all_upload_speeds, color="blue", width=WIDTH)

# Label the x-axis using the output of os.listdir(), which we used at the
# beginning of this script
plt.xticks([r + WIDTH * 1.5 for r in range(len(all_download_speeds))], network_names)

plt.ylabel("Network speed (Mbps)")
plt.legend(["Download", "Upload"], loc=2)

plt.title("Network performance")
plt.savefig("results")
