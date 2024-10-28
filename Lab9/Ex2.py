# Read from the survey_1000.csv file and calculate the average, max, and min values

import csv
import os

filename = 'survey_1000.csv'

if os.path.exists(filename) and os.access(filename, os.R_OK):
    file_size = os.path.getsize(filename)
    print(f"File Size: {file_size} bytes")

    line_number = 0
    total_RealInc = 0
    num_values = 0
    max_RealInc = 0
    min_RealInc = float('inf')  # Using infinity to find the minimum

    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for line in csv_reader:
            if line_number > 0:  
                RealInc = float(line[5456])  
                if RealInc > 0:
                    num_values += 1
                    total_RealInc += RealInc
                    max_RealInc = max(max_RealInc, RealInc)
                    min_RealInc = min(min_RealInc, RealInc)
            line_number += 1

    average = total_RealInc / num_values if num_values > 0 else 0

    print(f"Number of non-zero values: {num_values}")
    print(f"Average RealInc: ${round(average, 2)}")
    print(f"Min RealInc: ${min_RealInc}  Max RealInc: ${round(max_RealInc, 2)}")
else:
    print("File does not exist or is not readable.")