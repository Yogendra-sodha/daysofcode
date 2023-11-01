import pandas
name = pandas.read_csv("nato/nato_phonetic_alphabet.csv")
letter = list(name.letter.str.lower())    
code = list(name.code.str.lower())


nato_dict = {k:v for k,v in zip(letter,code)}

try:
    usr_input = input("Enter a name: ").lower()
    phonetic = [nato_dict[i] for i in usr_input]
except KeyError:
    print("Only numbers allowed")

else:
    print(phonetic)
