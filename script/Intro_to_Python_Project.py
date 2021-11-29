"""The main function to implement the project's function."""

import sys
# Change the absolute path if run on different laptops
# or put this project folder in the same position
sys.path.append(r'D:\Intro_to_Python_Project\my_module')

# The below code also works in the IDE, but not for the
# command line on the localhost
# sys.path.append(r'./my_module')

import functions
from classes import MyEmail

print('Welcome to the encryption email!')
functions.split_boundary()

while(True):
    print('Please choose a funtion: ')
    print('\t[1]Send an email')
    print('\t[2]Receive email(s)')
    print('\t[3]Quit')
    user_input = input('Your choice: ')
    print()

    if user_input == '1':
        functions.send_email(2)
    elif user_input == '2':
        functions.receive_email(2)
    elif user_input == 'Quit':
        break
    else:
        print('Invalid input! Please try again!\n')
