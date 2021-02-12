# setup a dictionary with states and capitals
# get user input
# print the value attached to the users input

states = {'Texas': 'Austin',
          'Florida': 'Sacramento',
          'Georgia': 'Atlanta'}


while True:
    user_input = input('Enter a state: ')
    print(states.get(user_input, "Not a state"))
