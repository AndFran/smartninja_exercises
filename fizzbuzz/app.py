
print "Welcome to fizzbuzz"

while True:
    try:
        choice = raw_input("Enter a number between 1 and 100 or q to quit: ")
        choice = choice.lower()
        if choice == 'q':
            break
        choice = int(choice)
        if choice < 1 or choice > 100:
            raise ValueError
    except ValueError:
        print "Please enter a valid number between 1 and 100"

    for i in range(1, choice+1):
        if i % 3 == 0 and i % 5 == 0:
            print 'fizzbuzz'
        elif i % 3 == 0:
            print 'fizz'
        elif i % 5 == 0:
            print 'buzz'
        else:
            print i
