#Step 1 
import random
word_list = ["aardvark", "baboon", "camel"]

#TODO-1 - Randomly choose a word from the word_list and assign it to a variable called chosen_word.

word = random.choice(word_list)
print(word)

#TODO-2 - Ask the user to guess a letter and assign their answer to a variable called guess. Make guess lowercase.
blanks = ['_'] * len(word)

i = 0
# camel = 0,1,2,3,4 = 5
while i<len(set(word)):
  user_input = input("Guess a word ").lower()

  k=0
  for j in range(len(word)):
    if word[j] == user_input:
      blanks[j] = user_input
      k+=1
  if k==0:
    i+=1
  print(blanks, 'turn left',len(set(word)) - i)
  if ''.join(blanks) == word:
    print("user won")
    break
  elif len(set(word)) - i == 0:
    print("Game over")
    break

  
    