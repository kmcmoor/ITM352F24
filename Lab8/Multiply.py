# Algorithm for multiplying two numbers

def multiply(x, y): # Takes x to the power of y
    product = 0
    for _ in range(y):  # The for loop goes again and again in the range of y
        product += x   # This adds the product to itself y times
    
    return product

first = int(input("Enter the first number: "))
second = int(input("Enter the second number: "))

prod = multiply(first, second)
print(f"The product of {first} and {second} is {prod}")