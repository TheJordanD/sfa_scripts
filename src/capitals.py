states = {'Texas': 'Austin',
          'Florida': 'Sacramento',
          'Georgia': 'Atlanta'}


while True:
    user_input = input('Enter a state: ')
    print(states.get(user_input, "Not a state"))
