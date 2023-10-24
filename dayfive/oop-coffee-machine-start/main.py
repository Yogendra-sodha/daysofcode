from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

server = CoffeeMaker()
cashier = MoneyMachine()
waiter = Menu()


machine = True
while machine:
    usr_inp = input("What would you like 1 espresso, 2 latte, 3 cappa, 4 report? ")
    if usr_inp == "report":
        server.report()
        cashier.report()
    elif usr_inp == "off":
        machine = False
    else:
        drink = waiter.find_drink(usr_inp)
        if server.is_resource_sufficient(drink):
            if drink and cashier.make_payment(drink.cost):
                server.make_coffee(drink)
                