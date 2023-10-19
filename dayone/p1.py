# tip calc

print("welcome to tip calc")
num = float(input("What is total bill? $"))
people = int(input("How many people will split the bill? "))
percentage = int(input("what percent? 10, 12 or 15"))
tipAmount = float(num * (percentage/100)) + num
total = round(float(tipAmount/people),1)
print("each person :$"+str(total))