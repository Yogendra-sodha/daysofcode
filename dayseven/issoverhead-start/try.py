from datetime import datetime



machine = True
i=0
while machine:
    time = int(float(str(datetime.now()).split(" ")[1].split(":")[2]))
    if time == 0:
        print("New minute")
        i+=1
        print(i)