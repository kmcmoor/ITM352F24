# Library of Handy reusable math functions

# Given two numbers, return the midpoint between them

def midpoint(num1, num2):
    return ((num1 + num2)/2)

def squareroot(num1):
    return (num1**0.5)

def exponent(num1, num2):
    return (num1**num2)

def max(num1, num2):
    if num1 > num2:
        return(num1)
    else:
        return(num2)
    
def min(num1, num2):
    if num1 < num2:
        return(num1)
    else:
        return(num2)
    
def apply_function(x, y, func):
    result = func(x, y)
    return f"The function {func.__name__} {x}, {y} = {result}"