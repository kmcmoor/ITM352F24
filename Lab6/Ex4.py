# Determine a movie price using the following rules: 
# The normal price is $14, 
# If someone is 65 or older, they pay $8, 
# If it is Tuesday, the price is $10 
# If it is a matinee, the price is $5 for seniors and $8 otherwise

movieprice = 14

age = int(input("Enter your age: "))

tuesday_question = input("Is it Tuesday? (yes/no): ")
tuesday = (tuesday_question == "yes")

matinee_question = input("Are you a matinee? (yes/no): ")
matinee = (matinee_question == "yes")

# Determine the lowest price for the person
if age >= 65:
    if matinee:
        movieprice = min(movieprice, 5)  
    else:
        movieprice = min(movieprice, 8)  
elif tuesday:
    movieprice = min(movieprice, 10)  
elif matinee:
    movieprice = min(movieprice, 8)  

print(f"The price of the movie is: ${movieprice}")