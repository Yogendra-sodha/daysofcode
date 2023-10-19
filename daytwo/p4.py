import random


rock = [[0,2],[0,1],[0,0]]
paper = [[1,0],[1,2],[1,1]]
scissors = [[2,1],[2,0],[2,2]]


# user input
user_input = int(input("What do you chose 0 for rock, 1 for paper, 2 for scissors? "))
# com input random
com_input = random.randint(0,2)
print(com_input)
# result
game = [user_input,com_input]

if game[0] == 0:
    if rock.index(game) == 0:
        print("won")
    elif rock.index(game) == 1:
        print("loose")
    else:
        print("draw")
elif game[0] == 1:
    if paper.index(game) == 0:
        print("won")
    elif paper.index(game) == 1:
        print("loose")
    else:
        print("draw")
else:
    if scissors.index(game) == 0:
        print("won")
    elif scissors.index(game) == 1:
        print("loose")
    else:
        print("draw")
