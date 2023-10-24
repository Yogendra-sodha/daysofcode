# generate unique values from data

from game_data import data
import random


a = random.randint(0,len(data)-1)
b = random.randint(0,len(data)-1)

def getDetails(idx):
  count = data[idx]['follower_count']
  return count

score = 0
game_on = True
c1 = getDetails(a)
while game_on:
  print("a :",data[a]['name'],",",data[a]['description'])
  print("VS")
  print("b :",data[b]['name'],",",data[b]['description'])
  inp = input("which has more follower a or b? ")
  c2 = getDetails(b)
  
  if inp == 'a' and c1 > c2:
    score +=1
    print("Your current score is: ",score)
    
  elif inp == 'b' and c2 > c1:
    score+=1
    print("Your current score is: ",score)
  else:
    print(c1,c2)
    print("Lost, Game over :(")
    game_on = False
    
  a = b
  c1 = c2
  b = random.randint(0,len(data)-1)