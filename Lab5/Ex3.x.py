# Create a dictionary from survey responses and IDs
survey_responses = [5, 7, 3, 8]
respondent_ids = (1012, 1035, 1021, 1053)

dictionary = dict(zip(respondent_ids, survey_responses))

print(dictionary)
