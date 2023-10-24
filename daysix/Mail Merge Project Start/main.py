#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".

filepath = "Mail Merge Project Start/Output/ReadyToSend/"

with open("Mail Merge Project Start/Input/Names/invited_names.txt",mode="r") as names:
    content_names = names.readlines()

invite_name = [i.strip('\n') for i in content_names]

paths = [filepath+i for i in invite_name]

with open("Mail Merge Project Start/Input/Letters/starting_letter.txt",mode="r") as letter_file:
    letter_content = letter_file.read()


for name,path in zip(invite_name,paths):
    temp = letter_content.replace("[name]",name)
    with open(path+".txt",mode = "w") as file:
        file = file.write(temp)