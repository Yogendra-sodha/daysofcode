############### Blackjack Project #####################

#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
  
game_start = input("Do you want to start a Game Y or N? ").lower()

def add(deck1,deck2):
  user_t = sum(deck1)
  com_t = sum(deck2)
  if user_t > com_t and user_t<=21:
    print("You won")
  elif user_t > com_t and user_t>=21:
    print("You lose")
  elif user_t < com_t and com_t>=21:
    print("You won")
  elif user_t < com_t and com_t<=21:
    print("You lose")
  else:
    print("draw")

def blackjack():
  # card dealing
  user_card = random.sample(cards,2)
  print("user card: ",user_card)
  computer_card = random.sample(cards,2)
  print("computer card: ",computer_card[0])

  # Hit or pass
  hit_pass = input("Do you want h or p? ").lower()

  # Hit 
  if hit_pass == "h":
    user_card.append(random.choice(cards))
    print("user card: ",user_card)
    print("computer card: ",computer_card)
    add(user_card,computer_card)
  
  # Pass
  else:
    print("user card: ",user_card)
    print("computer card: ",computer_card)
    add(user_card,computer_card)

  status = input("Do you want to play another game Y or N ").lower()
  if status == "y":
    blackjack()

blackjack()
    
    
    
      
      

      
      
  