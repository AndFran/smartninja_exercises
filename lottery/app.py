from random import sample

LOWER_BOUND = 1
UPPER_BOUND = 50


def generate_random_sample(amount):
    numbers = sample(range(LOWER_BOUND, UPPER_BOUND), amount)
    return numbers


def format_number_list(numbers):
    formatted = ", ".join([str(num) for num in numbers])
    return formatted


def main():
    while True:
        choice = raw_input("How many numbers would you like (q to quit): ")
        if choice.lower() == 'q':
            break
        try:
            choice = int(choice)
            if choice < LOWER_BOUND or choice >= UPPER_BOUND:
                print("Enter a number between {} and {}".format(LOWER_BOUND, UPPER_BOUND - 1))
                continue
        except ValueError:
            print("Enter a valid number of q to quit")
            continue

        random_sample = generate_random_sample(choice)
        print("Your numbers are {}".format(format_number_list(random_sample)))

        print("_" * 50)


if __name__ == '__main__':
    main()
