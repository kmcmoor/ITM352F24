# I referenced Exercise 2 to help me with this

import csv

total_fares = 0
num_fares = 0
max_trip_distance = 0

with open('taxi_1000.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    next(csv_reader)  

    for row in csv_reader:
        
        fare = float(row[0])  
        trip_miles = float(row[1])  

        if fare > 10:
            total_fares += fare
            num_fares += 1
       
        if trip_miles > max_trip_distance:
            max_trip_distance = trip_miles


average_fare = total_fares / num_fares if num_fares > 0 else 0

print(f"Total Fares: ${total_fares:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Maximum Trip Distance: {max_trip_distance} miles")
