#Create a function—call it squareroot—that takes a number and returns the squareroot of that number

def squareroot(num1):
    return (num1**0.5)

number1 = float(input("Enter the value:"))

sqr = squareroot(number1)
print("The squareroot of the value is: ", sqr)