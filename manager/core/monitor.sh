#!/bin/bash
if command -v free && command -v gawk
then
    free -h | gawk 'match($5,/[0-9]+G/){print $2,$3,$4}';
else
    memory=($(vmstat -h | awk '/[0-9]\.[0-9]G/{print $4,$5}'));
    memory_total=${memory[0]//G};
    memory_left=${memory[1]//G};
    memory_used=$(echo "($memory_total-$memory_left)" | bc -l);
    echo "${memory_total}G ${memory_used}G ${memory_left}G";
fi