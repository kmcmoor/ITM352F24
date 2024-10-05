# Write a program that asks the user for a year 
# and replies with either "leap year" or "not a leap year"

year = int(input("What is the year?"))

if (year % 4) == 0:
    print ("leap year")
elif year % 100 == 0:
    print("not a leap year")
elif year % 400 == 0:
    print("leap year")
else:
    print("not a leap year")
