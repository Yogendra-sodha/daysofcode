print("Welcome")
dir = input("Right or left? ")
if dir.lower() == "left":
    action = input("Swim or Wait")
    if action.lower() == "swim":
        print("Game over")
    else:
        door = input("which door red,blue,yellow? ")
        if door.lower() == "yellow":
            print("won")
        elif door.lower() == "red":
            print("fire")
        elif door.lower() == "blue":
            print("eaten")
        else:
            print("Game over")
else:
    print("game")