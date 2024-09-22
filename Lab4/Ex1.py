#Ask the user to enter their first name, middle initial and last name. Concatenate them together with spaces in between and print out the result.

First = input("Please enter your first name: ")
MiddleInitial = input("Please enter your middle initial: ")
Last = input("Please enter your last name: ")

FullName = First + " " + MiddleInitial + " " + Last
print("Your full name is:", FullName)
print(f"{First } {MiddleInitial } {Last}")
print("Your full name is %s %s %s" % (First, MiddleInitial, Last))