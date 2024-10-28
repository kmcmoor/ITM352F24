with open("Names.txt", mode="r") as textFile:
        line = textFile.readline()
        count = 1

        while line: 
                print(line)
                count += 1
                line = textFile.readline()

print (f"There are {count} names in the file")


# Using readline()
#with open("Names.txt", mode="r") as textFile:
#    count = 0
#    for line in textFile:
#        print(line.strip())  
#        count += 1
#    print(f"There are {count} names in the file")


try:
    with open("Names.txt", "r") as textFile:
        data = textFile.read()
        print(data)
except FileNotFoundError:
    print("File not found.")
except IOError:
    print("File is not readable.")


with open("Names.txt", "a") as textFile:
    textFile.write("Port, Dan\n")
