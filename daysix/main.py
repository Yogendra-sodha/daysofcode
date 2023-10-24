import turtle
import pandas as pd

# open csv file

data = pd.read_csv("50_states.csv")
stateList = list(data.state.str.lower())

screen = turtle.Screen()
screen.title("Us states")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
machine = True
while machine:
    score = 0
    usr_input = screen.textinput(title=str(score)+"/50",prompt="what is another state name").lower()
    if usr_input in stateList:
        temp = stateList.index(usr_input)
        stateList.pop(temp)
        score+=1
        x = int(data.loc[data.state.str.lower() == usr_input,'x'].values[0])
        y = int(data.loc[data.state.str.lower() == usr_input,'y'].values[0])
    else:
        print("Not in list or already taken")


# turtle.onscreenclick(x,y)

# turtle.mainloop()