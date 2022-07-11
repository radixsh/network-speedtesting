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

SUFFIX="${ROUTER_OR_EXTENDER}_${GHZ}"

# Initialize OUTPUT (which will populate the output file) with a header line
# stating the network being tested 
OUTPUT="${ROUTER_OR_EXTENDER} ${GHZ}\n"

# https://stackoverflow.com/questions/169511/how-do-i-iterate-over-a-range-of-numbers-defined-by-variables-in-bash
ITERS=5
for ((i=0;i<=ITERS;i++)) do
    echo -e "Running test ${i}..."
    # https://www.tecmint.com/assign-linux-command-output-to-variable/
    speedtest=$(speedtest)
  
    # https://stackoverflow.com/questions/13373249/extract-substring-using-regexp-in-plain-bash
    # https://stackoverflow.com/questions/33573920/what-does-k-mean-in-this-regex
    # https://stackoverflow.com/questions/8101701/grep-characters-before-and-after-match
    # https://overapi.com/regex
    info=$(echo ${speedtest} | grep -oh "\w*[A-Za-z]\+load: [0-9]\+[.][0-9]\+.\{0,7\}")
    echo -e "${info}\n"
    OUTPUT+="${info}\n\n"
done

# https://unix.stackexchange.com/questions/396161/how-to-use-variables-in-a-filename
echo -e ${OUTPUT} > "wifi_${SUFFIX}.txt"

less "wifi_${SUFFIX}.txt"
