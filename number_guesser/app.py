from random import randint


def main():
    secret = randint(1, 100)

    while True:
        print(secret)
        guess = raw_input("Enter a number between 1 and 99 (q to quit):")
        guess = guess.lower()
        if guess == 'q':
            exit(0)
        try:
            guess = int(guess)
            if guess == secret:
                print "YOU WIN"
                exit(0)
            elif guess > secret:
                print "You guess is too high"
            else:
                print "You guess is too low"
        except ValueError:
            print "Enter a valid number or q to quit"


if __name__ == '__main__':
    main()
