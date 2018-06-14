from __future__ import print_function
import csv
import os.path


class Car(object):
    def __init__(self, brand, model, km, service_date):
        self.brand = brand
        self.model = model
        self.km = km
        self.service_date = service_date

    def __str__(self):
        return "{}, {}, {}, {}".format(self.brand, self.model, str(self.km), self.service_date)


def read_all_cars():
    cars = []
    if not os.path.isfile('database.txt'):
        with open('database.txt', 'w+'):
            pass
    with open('database.txt', 'r') as f:
        rows = csv.reader(f)
        for row in rows:
            car = Car(row[0], row[1], float(row[2]), row[3])
            cars.append(car)
    return cars


def view_all_cars():
    print("================================")
    print("|        Car Rental App         |")
    print("================================")

    for car in all_cars:
        print("-", str(car))
    print("================================")


def check_field(input_message, min_length=-1, expected_type=None):
    while True:
        the_input = raw_input(input_message)
        if min_length > -1:
            if len(the_input) < min_length:
                print("You must enter more text minimum length is", min_length)
                continue
        if expected_type is not None:
            try:
                the_input = expected_type(the_input)
            except ValueError:
                print("Please enter a valid value")
                continue
        return the_input


def build_new_car():
    brand = check_field("Enter brand:", min_length=1)
    model = check_field("Enter model:", min_length=1)
    km = check_field("Enter km:", expected_type=float)
    service_date = check_field("Enter service date:")
    new_car = Car(brand, model, km, service_date)
    return new_car


def add_new_car():
    car = build_new_car()
    all_cars.append(car)
    write_changes()


def write_changes():
    with open('database.txt', 'w+') as f:
        writer = csv.writer(f)
        for c in all_cars:
            writer.writerow([c.brand, c.model, c.km, c.service_date])


def edit_car():
    while True:
        for index, c in enumerate(all_cars, start=1):
            print(index, " - ", str(c))
        try:
            choice = raw_input("Enter car number (q to quit):")
            if choice.lower() == 'q':
                break
            choice = int(choice)
            if choice < 1 or choice > index:
                print("Please enter a number between 1 and", index)
                continue
        except ValueError:
            print("Please enter a valid number")
        car = build_new_car()
        all_cars[choice - 1] = car
        write_changes()
        break


main_menu_functions = {
    "1": view_all_cars,
    "2": edit_car,
    "3": add_new_car,
}


def main_menu():
    while True:
        print("================================")
        print("|        Car Rental App         |")
        print("================================")
        print("     1 - View all cars          ")
        print("     2 - Edit car               ")
        print("     3 - Add new vehicle        ")
        print("     4 - Quit                   ")
        print("================================")

        choice = raw_input("Enter menu choice:")
        if choice in main_menu_functions:
            main_menu_functions[choice]()
        elif choice == '4':
            exit(0)
        else:
            print("**Please enter an option from the menu**")


# load all cars
all_cars = read_all_cars()

if __name__ == '__main__':
    main_menu()
