import random


def generate_random_numbers():
    return random.sample(range(1, 10), 3)


def check_input():
    random_numbers = generate_random_numbers()
    print(random_numbers)
    print("I'm thinking of 3 numbers from 1 to 10. Guess one of them. ")
    user_input = input("Your guess: ")

    if user_input == 'q':
        quit()
    elif not user_input.isnumeric():
        print("Sorry, but I was really thinking of "
              + str(random_numbers[0])
              + ", " + str(random_numbers[1])
              + " and " + str(random_numbers[2]))
        quit()
    elif int(user_input) in random_numbers:
        print("You’re a mind reader!  My secret numbers were "
              + str(random_numbers[0])
              + ", " + str(random_numbers[1])
              + " and " + str(random_numbers[2]))
        return True
    else:
        print("Sorry, but I was really thinking of "
              + str(random_numbers[0])
              + ", " + str(random_numbers[1])
              + " and " + str(random_numbers[2]))
        quit()


while check_input():
    check_input()
