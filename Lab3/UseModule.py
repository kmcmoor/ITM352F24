# Program to test the use of the HandyMath library
import HandyMath as HM

number1 = input("Enter first value: ")
number2 = float(input("Enter second value: "))
number1 = float(number1)


mid = HM.midpoint(number1, number2)
print("The midpoint is: ", mid)

sqr = HM.squareroot(number1)
print("The squareroot of the first value is: ", sqr)

exp = HM.exponent(number1, number2)
print("The result of raising ", number1, "to the power of ", number2, "is: ", exp)

mx = HM.max(number1, number2)
print("The max of the two numbers is: ", mx)

mn = HM.min(number1, number2)
print("The min of the two numbers is: ", mn)