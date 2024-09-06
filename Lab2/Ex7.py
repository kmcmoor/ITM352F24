# Ask user to input a temperature in degrees Farenheit.
# Convert that temperature to Cellsius and output it.

degreesF = input ("Enter a temperature in Farenheit: ")
degreesC = (float (degreesF) - 32) * .55

print ("This converts to ", degreesC, "Celsius")