"""Five functions to realize the functionalities of email and encryption."""

import email
import smtplib
import imaplib
from email.header import decode_header
from email.mime.text import MIMEText
from classes import MyEmail

def split_boundary():
    """Print fifty equal signs to create a boundary."""

    print('=' * 50,'\n')


def send_email(offset_num, direction = 'right'):
    """Send an email from the valid user to one or more receivers.

    Parameters
    ----------
    offset_num : int
        The number that each character in the string to shift.
    direction : str, optional
        The direction that characters will shift. default = 'right'

    Sources
    -------
        I cited some codes from the below link. I have understood them
        and modified them as many as I can by using the Email class.
        https://blog.csdn.net/qq_30595441/article/details/105242892
    """

    # Create an MyEmail object
    email_obj = MyEmail()

    # While-loop1. Check the input username
    flag1 = False
    while not flag1:
        print('Please enter the username: ')
        user_name = input()
        # Call user_check method to process the input username and
        # assign the return boolean value to `flag1`
        flag1 = email_obj.user_check(user_name)

    # While-loop2. Check each receivers' email address
    flag2 = False
    while not flag2:
        print("Please enter the receivers' emails (enter 'Quit' to exit): ")
        receiver = input()
        flag2 = email_obj.user_check(receiver, 'receiver')

        # Check if `flag2` is True, there are two situations
        if flag2 == True:
            # Check if the `receiver` is 'Quit', terminate the loop
            if receiver == 'Quit':
                break
            # Check if the `receiver` is valid, append it to the list
            # and reassign `flag2` to False and continue looping
            else:
                email_obj.receivers.append(receiver)
                flag2 = False
    split_boundary()

    # Write subject
    print('Please write the email subject: ')
    email_obj.mail_subject = input()
    email_obj.mail_subject = email_obj.mail_subject.title()
    encoded_subject = encode_email(email_obj.mail_subject, offset_num, direction)
    print()

    # Write content
    print('Please write the email contents: ')
    email_obj.mail_content = input()
    encoded_content = encode_email(email_obj.mail_content, offset_num, direction)
    split_boundary()

    # Assign email information
    # Cited codes that have been modified
    # https://blog.csdn.net/qq_30595441/article/details/105242892
    message = MIMEText(encoded_content, 'plain', 'utf-8')
    message['Subject'] = encoded_subject
    message['From'] = user_name
    message['To'] = ','.join(email_obj.receivers)

    # Use SMTP to send an email
    # Cited codes that have been modified
    # https://blog.csdn.net/qq_30595441/article/details/105242892
    try:
        smtp_obj = smtplib.SMTP(email_obj.send_server, email_obj.port)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(email_obj.user_name, email_obj.app_password)
        smtp_obj.sendmail(user_name, email_obj.receivers, message.as_string())
        smtp_obj.quit()
        print('Send successfully!')
    except:
        print('Assert error! Please check the server setting...')


def receive_email(try_num, receive_num = 1):
    """Receive receive_num email(s) from the valid user address.
       And determine to decode each part of it or not.

    Parameters
    ----------
    try_num : int
        The numeber of times attempted to decode and get the correct information.
    receive_num : int, optional
        The number of email wanted to receive. default = 1

    Sources
    -------
        I cited the following codes from the below link. I have modified most of
        them and deleted the 'HTML' and attachment conditionals since I think it
        is not the key point in this project.
        https://www.thepythoncode.com/article/reading-emails-in-python
    """

    email_obj = MyEmail()

    # Check the input username
    flag1 = False
    while not flag1:
        print('Please enter the username: ')
        user_name = input()
        flag1 = email_obj.user_check(user_name)

    # Create an IMAP4 class with SSL and login
    imap_obj = imaplib.IMAP4_SSL(email_obj.receive_server)
    imap_obj.login(email_obj.user_name, email_obj.app_password)

    # Get information from the Index box
    status, messages = imap_obj.select('INBOX')
    messages = int(messages[0])

    for i in range(messages, messages - receive_num, -1):
        # Fetch the email message by ID
        res, msg = imap_obj.fetch(str(i), '(RFC822)')

        for response in msg:
            if isinstance(response, tuple):
                # Parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])

                # Decode the email subject
                subject, encoding_1 = decode_header(msg['Subject'])[0]
                # Decode email sender
                from_sender, encoding_2 = decode_header(msg.get('From'))[0]

                # If subject is a bytes, decode to str
                if isinstance(subject, bytes):              
                    subject = subject.decode(encoding_1)
                    # From 1 to try_num, try try_num times to decode
                    # each time, the offset_num equals the actual try_num value
                    # in the interval [1, try_num]
                    for offset_num in range(1, try_num + 1):
                        decoded_subject = decode_email(subject, offset_num)
                        print('Subject:', decoded_subject)
                    print()

                # If from_sender is a bytes, decode to str
                elif isinstance(from_sender, bytes):
                    from_sender = from_sender.decode(encoding_2)
                    print('From:', from_sender)
                    print()

                # Else, the email is a plain text version
                else:
                    for offset_num in range(1, try_num + 1):
                        decoded_subject = decode_email(subject, offset_num)
                        print('Subject:', decoded_subject)
                    print()
                    print('From:', from_sender)
                    print()

                split_boundary()

                # If the email message is multipart
                if msg.is_multipart():
                    # Iterate over email parts
                    for part in msg.walk():
                        # Extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get('Content-Disposition'))
                        try:
                            # Get the email body
                            body = part.get_payload(decode = True).decode()
                        except:
                            pass

                        if content_type == 'text/plain' and 'attachment' not in content_disposition:
                            # Print text/plain emails and skip attachments
                            for offset_num in range(1, 1 + offset_num):
                                decoded_body = decode_email(body, offset_num)
                                print('Content: \n', decoded_body)
                            print()
                else:
                    # Extract content type of email
                    content_type = msg.get_content_type()
                    # Get the email body
                    body = msg.get_payload(decode = True).decode()

                    if content_type == 'text/plain':
                        # Print only text email parts
                        for offset_num in range(1, 1 + offset_num):
                            decoded_body = decode_email(body, offset_num)
                            print('Content: \n', decoded_body)
                        print()

                split_boundary()
    # Close the connection and logout
    imap_obj.close()
    imap_obj.logout()


def encode_email(input_string, offset_num, direction = 'right'):
    """Encode the input email in terms of Caesar cipher algorithm.

    Notes
    -----
    If input 'no', then the input information will not be encoded.

    Else, encode the `input_string` according to particular offset
    and shift direction. For letters, using the Caesar cipher algorithm;
    for other characters, simply shift based on the code point.

    Parameters
    ----------
    input_string : str
        The string wanted to be encoded.
    offset_num : int
        The number that each character in the string to shift.
    direction : str, optional
        The direction that characters will shift. default = 'right'

    Returns
    -------
    output_string : str
        The encoded or not encoded string we got.
    """

    output_string = ''

    # Choose to encode or not
    determine = input('Encode this or not? Enter yes or no: ')
    print()

    if determine == 'no':
        output_string = input_string

    elif determine == 'yes':
        # Right shift
        if direction == 'right':
            for char in input_string:
                code_point = ord(char)
                # Lowercase letters
                if ord('a') <= code_point <= ord('z'):
                    output_string += chr((code_point + offset_num - ord('a')) % 26 + ord('a'))
                # Uppercase letters
                # Z + 1 -> A
                # (90 + 1 - 65) % 26 + 65 = 0 + 65
                elif ord('A') <= code_point <= ord('Z'):
                    output_string += chr((code_point + offset_num - ord('A')) % 26 + ord('A'))
                # Other characters
                else:
                    output_string += chr(code_point + offset_num)
        # Left shift
        elif direction == 'left':
            for char in input_string:
                code_point = ord(char)
                if ord('a') <= code_point <= ord('z'):
                    # A - 1 -> Z
                    # (65 - 1 - 65 + 26) % 26 + 65 = 25 + 65
                    # B - 1 -> A
                    # (66 - 1 - 65 + 26) % 26 + 65 =  0 + 65
                    output_string += chr((code_point - offset_num - ord('a') + 26) % 26 + ord('a'))
                elif ord('A') <= code_point <= ord('Z'):
                    output_string += chr((code_point - offset_num - ord('A') + 26) % 26 + ord('A'))
                else:
                    output_string += chr(code_point - offset_num)

    return output_string


def decode_email(input_string, offset_num, direction = 'left'):
    """Decode the input email in terms of Caesar cipher algorithm.

    Notes
    -----
    If input 'no', then the input information will not be decoded.

    Else, decode the `input_string` according to particular offset
    and shift direction. For letters, using the Caesar cipher algorithm;
    for other characters, simply shift based on the code point.

    Parameters
    ----------
    input_string : str
        The string wanted to be decoded.
    offset_num : int
        The number that each character in the string to shift.
    direction : str, optional
        The direction that characters will shift. default = 'left'

    Returns
    -------
    output_string : str
        The decoded or not decoded string we got.

    """

    output_string = ''
    # Choose to decode or not
    determine = input('Decode this or not? Enter yes or no: ')

    if determine == 'no':
        output_string = input_string

    elif determine == 'yes':
        # Left shift
        if direction == 'left':
            for char in input_string:
                code_point = ord(char)
                if ord('a') <= code_point <= ord('z'):
                    # A - 1 -> Z
                    # (65 - 1 - 65 + 26) % 26 + 65 = 25 + 65
                    # B - 1 -> A
                    # (66 - 1 - 65 + 26) % 26 + 65 =  0 + 65
                    output_string += chr((code_point - offset_num - ord('a') + 26) % 26 + ord('a'))
                elif ord('A') <= code_point <= ord('Z'):
                    output_string += chr((code_point - offset_num - ord('A') + 26) % 26 + ord('A'))
                else:
                    output_string += chr(code_point - offset_num)
        # Right shift
        elif direction == 'right':
            for char in input_string:
                code_point = ord(char)
                # Lowercase letters
                if ord('a') <= code_point <= ord('z'):
                    output_string += chr((code_point + offset_num - ord('a')) % 26 + ord('a'))
                # Uppercase letters
                # Z + 1 -> A
                # (90 + 1 - 65) % 26 + 65 = 0 + 65
                elif ord('A') <= code_point <= ord('Z'):
                    output_string += chr((code_point + offset_num - ord('A')) % 26 + ord('A'))
                # Other characters
                else:
                    output_string += chr(code_point + offset_num)

    return output_string
