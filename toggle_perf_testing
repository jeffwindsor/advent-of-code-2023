#!/bin/bash

# Toggle AOC_PERF between 0 and 1, report current setting

current_value="${AOC_PERF:-0}"

if [ "$current_value" = "1" ] || [ "$current_value" = "true" ] || [ "$current_value" = "yes" ]; then
    export AOC_PERF=0
    echo "AOC Performance Metrics: OFF"
else
    export AOC_PERF=1
    echo "AOC Performance Metrics: ON"
fi

# Show current setting
echo "Current value: AOC_PERF=$AOC_PERF"
