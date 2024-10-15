# Instructions:
# Build an interactive quiz that:
# 1. Asks a user multiple-choice questions, with four answer options (a-d)
# 2. If a user enters any other response, such as "q", it should be ignored and the user should be re-prompted
# 3. Let them know if their answer is correct or not
# 4. At the end of the quiz, it should report the final score
# 5. Write the history of scores out to a file
# 6. Notify the user when they get a new high score

import datetime # To create a time stamp


QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "11", "8", "14"],
    "What is the capital of Texas": ["Austin", "San Antonio", "Dallas", "Houston"],
    "The Last Supper was painted by which artist": ["Da Vinci", "Rembrandt", "Picasso", "Michelangelo"]
}

# Initializing the variable, score, to keep track of the number of correct answers
score = 0

for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    sorted_alternatives = sorted(alternatives)
    
    # Present the user four answer options (a-d)
    labels = ['a', 'b', 'c', 'd']
    
    for i in range(len(sorted_alternatives)):
        print(f"{labels[i]}: {sorted_alternatives[i]}") # Print each answer option with the letters a-d

    # valid_input is the variable used to check if what the user inputs is valid, the while loop is to keep reprompting the user until they enter a valid answer
    valid_input = False
    while not valid_input:

    # Converting the user's answer to lowercase
        answer_label = input(f"{question}? ").lower()

        # This is if the user inputs a-d
        if answer_label in labels:
            # index is used to find the position of the letter the user entered in the list of labels
            answer_index = labels.index(answer_label)
            # To retrieve the answer option based on the index
            answer = sorted_alternatives[answer_index]
            # To exit the while loop
            valid_input = True 
        # This is if the user inputs something other than a-d
        else:
            print("Invalid input. Please choose a, b, c, or d.")

    if answer == correct_answer:
        print("Correct!")
        # Adding 1 point for each correct answer
        score += 1
    else:
        print(f"The correct answer is {correct_answer!r}, not {answer!r}")

# Reporting the final score at the end of the quiz
print(f"Your final score is: {score} out of {len(QUESTIONS)}")

# Write the history of scores out to a file
# I used W3schools to help! It's under the File Handling section, and says Python Write/Create Files
f = open("scorehistory.txt", "a")  # Opens a new file
f.write(f"{datetime.datetime.now()}: {score} out of {len(QUESTIONS)}\n")  # Writes the score with a timestamp
f.close()  # Closes the file
