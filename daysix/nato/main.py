student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}


import pandas
student_data_frame = pandas.DataFrame(student_dict)
name = pandas.read_csv("nato_phonetic_alphabet.csv")
letter = list(name.letter.str.lower())    
code = list(name.code.str.lower())


#TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}

nato_dict = {k:v for k,v in zip(letter,code)}


#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

usr_input = input("Enter a name: ").lower()

phonetic = [nato_dict[i] for i in usr_input]
print(phonetic)