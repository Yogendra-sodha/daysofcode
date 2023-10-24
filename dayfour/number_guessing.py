# has a number
# ask difficulty level 
# ask for guess the number
# counts the attempt
import random
EASY = 10
HARD = 5

def diff(level):
    if level[0] == "e":
        return EASY
    else:
        return HARD
    

def game():
    ANS = random.randint(1,100)
    print("The number is between 1 and 100")
    level = input("what is your difficuly level easy or hard? ").lower()

    attempts = diff(level)

    for i in range(attempts):
        print("You have",attempts-i,"left guess the number",end = " ")
        user_input = int(input())
        if user_input == ANS:
            print("You won")
            break
        elif user_input > ANS:
            print("Too high")
        else:
            print("Too low")
    print(ANS)
    status = input("Do you want to play another game Y or N ").lower()
    if status == "y":
        game()

game()