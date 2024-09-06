# Ask the user to enter an arbitrary sentence. Calculate the length of that 
# string and return that value

sentence = input ("Enter a sentence: ")

string_length = len(sentence)
output_string = "You entered \"" + sentence + "\". It has length " + str(string_length)
print (output_string)