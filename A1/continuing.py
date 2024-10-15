
QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "11", "8", "14"],
    "What is the capital of Texas": ["Austin", "San Antonio", "Dallas", "Houston"],
    "The Last Supper was painted by which artist": ["Da Vinci", "Rembrandt", "Picasso", "Michelangelo"]
}


for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    sorted_alternatives = sorted(alternatives)
 
    labels = ['a', 'b', 'c', 'd']

    for i in range(len(sorted_alternatives)):
        print(f"{labels[i]}: {sorted_alternatives[i]}")  

    valid_input = False
    
    while not valid_input:
        answer_label = input(f"{question}? ").lower()
 
        if answer_label in labels:
            answer_index = labels.index(answer_label)
            answer = sorted_alternatives[answer_index]
            valid_input = True  
        else:
            print("Invalid input. Please choose a, b, c, or d.")

    if answer == correct_answer:
        print("Correct!")  
    else:
        print(f"The correct answer is {correct_answer!r}, not {answer!r}")
