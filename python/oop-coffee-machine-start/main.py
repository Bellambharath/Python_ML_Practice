from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()
# menu_item = MenuItem()

coffee_maker.report()
my_money_machine.report()

is_on = True

while is_on:
    items = menu.get_items()
    choice = input(f"What would you like? {items}:").lower()
    if choice == 'off':
        is_on = False
    elif choice == 'report':
        coffee_maker.report()
        my_money_machine.report()
    else:
        drink = menu.find_drink(choice)

        if coffee_maker.is_resource_sufficient(drink):

            if my_money_machine.make_payment(drink.cost):
                print("Transaction is Successfully")
                coffee_maker.make_coffee(drink)
            else:
                print("Transaction was Unsuccessfully")


