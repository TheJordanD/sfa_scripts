import random


def generate_random_numbers():
    numbers = random.sample(range(1, 10), 3)
    print(numbers)
    print("I'm thinking of 3 numbers from 1 to 10. Guess one of them. ")

    return numbers


def end_game(numbers):
    print("Sorry, but I was really thinking of "
          + str(numbers[0])
          + ", " + str(numbers[1])
          + " and " + str(numbers[2]))
    quit()


while True:
    random_numbers = generate_random_numbers()
    user_input = input("Your guess: ")

    if user_input == 'q':
        quit()
    elif not user_input.isnumeric():
        print(user_input + " is not a number")
        end_game(random_numbers)
    elif int(user_input) in random_numbers:
        print("You’re a mind reader!  My secret numbers were "
              + str(random_numbers[0])
              + ", " + str(random_numbers[1])
              + " and " + str(random_numbers[2]))
    else:
        end_game(random_numbers)
