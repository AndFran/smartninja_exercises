
print("Welcome to menu planner")

menu = {}

while True:
    try:
        dish = raw_input("Enter a dish (q to quit):")
        if dish == 'q' or dish == 'Q':
            break
        price = raw_input("Enter a price:")
        price = float(price)
        menu[dish] = price
    except ValueError:
        print("Enter a valid name and price")

if len(menu) > 0:
    with open('menu_file.txt', 'w+') as f:
        for key, value in menu.items():
            f.write(key+","+str(value)+"\n")
