# print report() == availabe resources
# check resource
# latter, espresso = select coffee
# add coin == value more than cost give diff in change
#  give coffee and change

from coffee_data import resources,items,profit

def money_insert():
    quarter = int(input("How many qurters? "))
    nickel = int(input("How many nickel? "))
    dimes = int(input("How many dimes? "))
    penny = int(input("How many penny? "))
    return quarter,nickel,dimes,penny

def money_counter(q,n,d,p):
    money = round(q*0.25 + n*0.10 + d*0.05 + p*0.01,2)
    return money


def check_resources(usr_inp):
    required_items = items[usr_inp]["ingredients"]
    for i in required_items:
        # check resources
        if resources[i] < required_items[i]:
            return False
        else:
            resources[i] -=required_items[i]
    print(resources)
    return True
        

def money_check(money,usr_inp):
    if money < items[usr_inp]["cost"]:
        return False,money
    else:
        money -=items[usr_inp]["cost"]
        global profit
        profit = profit + items[usr_inp]["cost"]
        return True,money
    
machine = True
while machine:
    usr_inp = input("What would you like 1 espresso, 2 latte, 3 cappa, 4 report? ")
    mn = 0
    if usr_inp == 4:
        print(resources)
        print(profit)
        continue
    elif usr_inp == "off":
        machine = False
    else:
        usr_inp = int(usr_inp)
        if check_resources(usr_inp):
            q,w,e,r = money_insert()
            check,rem_money = money_check(money_counter(q,w,e,r),usr_inp)
            if check:
                print("Here is your coffee")
                print("here is your change",rem_money)
            else:
                print("Not enough money")
                print("Here is your refund",rem_money)
        else:
            print("Not enough resources to make your item")







