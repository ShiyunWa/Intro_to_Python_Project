"""A customized class for basic email information."""

from re import match

class MyEmail():
    """A class used to represent email information."""

    def __init__(self):
        """
        Parameters
        ----------
        send_server : str
            The server used to send an email. default = 'smtp.gmail.com'.
        receive_server : str
            The server used to receive an email. default = 'imap.gmail.com'.
        app_password : str
            The application password for the particular user. default = 'qedwovadjvqairbb'.
        user_name : str
            The username of the valid user. default = 'shiyunwa@gmail.com'.
        port : int
            The port number for the specific email server. default = 587.
        receivers : list
            Email addresses to receive emails. default = [].
        mail_subject : str, optional
            Email subject wanted to send. default = ''.
        mail_content : str, optional
            Email content wanted to send. default = ''.
        """

        self.send_server = 'smtp.gmail.com'
        self.receive_server = 'imap.gmail.com'
        self.app_password = 'qedwovadjvqairbb'
        self.user_name = 'shiyunwa@gmail.com'
        self.port = 587
        self.receivers = []
        self.mail_subject = ''
        self.mail_content = ''

    def user_check(self, input_string, choice='sender'):
        """Check the input user's email format.

        Notes
        -----
        If the argument `choice` isn't passed in, the default choice
        'sender' is used. Then check whether the input information is
        an email format or not; is equal to the preset username or not.
        If input the valid username, print the welcome sentence and return
        true; otherwise, return false.

        Else if the argument `choice` is `receiver`，then check whether the
        input string is 'Quit' or not; is the input information is a correct
        email format or not.

        Parameters
        ----------
        input_string : str
            The input email string.
        choice : str, optional
            The user type that will be checked. default ='sender'.

        Return
        ------
        output_bool : bool
            True or False to determine the while-loop process.
        """

        # Trim whitespace in the input_string
        if ' ' in input_string:
            input_string = input_string.replace(' ', '')

        # Sender check
        if choice == 'sender':
            # Check the regular emial format by using regular expression
            if (match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+$', input_string) == None or
                input_string == None):
                print('Please enter the valid Gmail username!\n')
                output_bool = False
            # Check if it is the valid username
            elif input_string != self.user_name:
                print('You are not the valid user!\n')
                output_bool = False
            # input_string == self.user_name
            else:
                print('Welcome, Shiyun!')
                print('=' * 50, '\n')
                output_bool = True

        # Receiver check
        elif choice == 'receiver':
            # Check if input 'Quit'
            if input_string == 'Quit':
                output_bool = True
            # Check the regular emial format by using regular expression
            elif (match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+(\.[a-zA-Z]+)+$', input_string) == None or
                input_string == None):
                print("Please enter the valid receiver's email!\n")
                output_bool = False
            # Other valid email inputs
            else:
                output_bool = True

        return output_bool
