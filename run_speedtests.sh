#!/bin/bash

# Input validation
# https://stackoverflow.com/questions/10552711/how-to-make-if-not-true-condition
if ! [ $# -eq 2 ] 
then
    echo "Usage: ./run_speedtests.sh <router OR extender> <band-type>"
    exit 1
fi

ROUTER_OR_EXTENDER=$1
GHZ=$2
# This will be the name of the output file
OUTPUT_FILE="${ROUTER_OR_EXTENDER}_${GHZ}"

# Initialize OUTPUT (which will populate the output file) with a header line
OUTPUT="${ROUTER_OR_EXTENDER} ${GHZ}\n"
# Ensure existence of a subdirectory to hold the output file
# https://stackoverflow.com/questions/793858/how-to-mkdir-only-if-a-directory-does-not-already-exist
mkdir -p data/

# https://stackoverflow.com/questions/169511/how-do-i-iterate-over-a-range-of-numbers-defined-by-variables-in-bash
ITERS=5
echo -e "${ITERS} tests will run, one by one, and by the nature of how speedtests
work, they will take a little while. I suggest alt-tabbing away for a bit.\n"

for ((i=0;i<=ITERS;i++)) do
    echo -e "Running test ${i}..."
    # https://www.tecmint.com/assign-linux-command-output-to-variable/
    speedtest=$(speedtest)

    # https://stackoverflow.com/questions/13373249/extract-substring-using-regexp-in-plain-bash
    # https://stackoverflow.com/questions/33573920/what-does-k-mean-in-this-regex
    # https://stackoverflow.com/questions/8101701/grep-characters-before-and-after-match
    # https://overapi.com/regex
    download=$(echo ${speedtest} | grep -oh "\w*Download: [0-9]\+[.][0-9]\+.\{0,7\}")
    upload=$(echo ${speedtest} | grep -oh "\w*Upload: [0-9]\+[.][0-9]\+.\{0,7\}")
    echo -e "${download}\n${upload}\n"
    OUTPUT+="${download}\n${upload}\n\n"
done

# https://unix.stackexchange.com/questions/396161/how-to-use-variables-in-a-filename
echo -e ${OUTPUT} > "data/${OUTPUT_FILE}.txt"
