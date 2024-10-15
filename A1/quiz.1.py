# First version of the quiz game

answer = input("What is the airspeed of a unladen swallow in miles/hr?: ")

if answer == '12':
    print("Correct!")
else:
    print(f"The answer is '12', not {answer!r}")

answer = input("What is the capital of Texas?: ")
if answer == "Austin":
    print("Correct!")
else:
    print(f"The answer is 'Austin', not {answer!r}")