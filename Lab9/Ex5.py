# Save the dictionary of quiz questions as a JSON file
import json

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "11", "8", "14"],
    "What is the capital of Texas": ["Austin", "San Antonio", "Dallas", "Houston"],
    "The Last Supper was painted by which artist": ["Da Vinci", "Rembrandt", "Picasso", "Michelangelo"]
}

# Specify the name of the JSON file
filename = "quiz.json"

# Open the file in write mode and save the dictionary as JSON
with open(filename, "w") as DictFile:
    json.dump(QUESTIONS, DictFile, indent=4)

print(f"Data has been written to {filename}")