import random
import pyperclip
import cryptography
from cryptography.fernet import Fernet
import string
import webbrowser
import os
import statistics
import matplotlib.pyplot as plt

running = True
root = False
root_login = True


def load_key():
    with open('key.key', 'rb') as file:
        key = file.read()
    return key


def reset_passwords():
    with open('SavedPasswords.txt', 'w') as f:
        f.write('')
    print('SavedPasswords.txt wiped.')


def reset_maindata():
    with open('MainData.txt', 'w') as f:
        f.write('')
    print('MainData.txt wiped.')


try:
    key = load_key()
except:
    print('No key.key file found.')
    y_or_n = input('Generate a new key.key file?(y/n) >>> ').lower()
    if y_or_n == 'y' or y_or_n == 'yes':
        new_key = Fernet.generate_key()
        with open('key.key', 'wb') as f:
            f.write(new_key)
        key = load_key()
        print('New key.key file setup and loaded')

        y_or_n = input('''
Because new key generated, master password and all other encrypted settings and data 
should be wiped unless you think you can recover your lost key.key file. 
Reset All Data?(y/n) >>> ''')
        if y_or_n == 'y' or y_or_n == 'yes':
            reset_maindata()
            reset_passwords()
        else:
            print('No data wiped. Try to recover old key.key file or reset data.')
    else:
        print('No new file generated.')
        y_or_n = input('Close Program to prevent errors? >>> ')
        if y_or_n == 'y' or y_or_n == 'yes':
            running = False

fer = Fernet(key)


def encrypt(to_be_encrypted):
    return fer.encrypt(to_be_encrypted.encode()).decode()


def decrypt(to_be_decrypted):
    return fer.decrypt(to_be_decrypted.encode()).decode()


# Stores the contents of the MainData File
with open('MainData.txt', 'r') as f:
    main_data_encrypt = f.readlines()
main_data = []
for index in main_data_encrypt:
    index = index.rstrip()
    index = decrypt(index)
    main_data.append(index)

try:
    root_pass = main_data[0].rstrip()
except:
    with open('MainData.txt', 'w') as f:
        f.write(encrypt('123'))
    with open('MainData.txt', 'r') as f:
        root_pass_encrypt = f.readlines(1)
    print('No root password found. Reset to 123')
    root_pass = decrypt(root_pass_encrypt[0].rstrip())

while root_login:
    user_attempt = input("Enter the root password or press enter to skip >>> ")
    if user_attempt == root_pass:
        print('Root Access Granted')
        root = True
        root_login = False

    else:
        print('Root Access Skipped. Some commands will not be available.')
        root_login = False

print("Welcome to Ark's Multifunctional Custom Command Line or MFCCL. Type 'h' for a list of useful commands")
while running:
    command = input('>>> ').lower()
    if command == 'h' or command == 'help':
        if root:
            print('Root Mode Enabled')
        print('''
* = Root Only Command. 
$ = Linux Only Command. (Normally needs to be manually configured for your linux flavour) (Default is xfce4-terminal)
(h)elp > Shows a list of useful commands.
(q)uit > Stops the program.
*showpass > Shows all current passwords that are saved.     
*newpass > Adds a new password.
*removepass > Removes a password.
genpass > Generates a random secure password from 8-16 characters long.
*newroot > Allows the user to change the root password.
root > Allows the user to retry root login.
webbrowser > Opens the default web browser to google.
*resetmaindata > WILL RESET ALL DATA STORED IN THIS FILE INCLUDING ROOT PASS AND OTHER SETTINGS. 
*resetsavedpasswords > WILL RESET ALL DATA STORED IN THIS FILE.
dataset > Calculates useful information about a data set.
*createfile > Creates a file at a specified path with a specified name and extension.
$terminal > Opens a Linux terminal and runs the command that you specify.
thank_you! > Thank your program!
        ''')
    elif command == 'q' or command == 'quit':
        print('Goodbye!')
        running = False

    elif command == 'showpass':
        if root:
            with open('SavedPasswords.txt', 'r') as f:
                all_pass_encrypt = f.readlines()
            all_pass = []

            if len(all_pass_encrypt) == 0:
                print('No Passwords. Type "newpass" to add a new account')
                continue
            else:
                for index in all_pass_encrypt:
                    try:
                        print(decrypt(index.rstrip()))
                    except cryptography.fernet.InvalidToken:
                        pass
        else:
            print('No Root Access.')

    elif command == 'newpass':
        if root:
            new_label = input('What label do you want for this account? >>> ')
            new_user_email = input('What is the username/email/phone-number for this account? >>> ')
            new_pass = input('What is the password for this account? >>> ')
            y_or_n = input(f'Is this correct?(y/n)\n{new_label}\n{new_user_email}\n{new_pass}\n>>> ')
            if y_or_n == 'y' or y_or_n == 'yes':
                with open('SavedPasswords.txt', 'r') as f:
                    saved_passes = f.readlines()
                if len(saved_passes) == 0:
                    with open('SavedPasswords.txt', 'a') as f:
                        f.write(encrypt(new_label))
                        f.write('\n' + encrypt(new_user_email))
                        f.write('\n' + encrypt(new_pass))
                        f.write('\n' + encrypt('|'))
                        print('Account added.')
                else:
                    with open('SavedPasswords.txt', 'a') as f:
                        f.write('\n' + encrypt(new_label))
                        f.write('\n' + encrypt(new_user_email))
                        f.write('\n' + encrypt(new_pass))
                        f.write('\n' + encrypt('|'))
                        print('Account added.')
            else:
                print('Account not added.')
        else:
            print('No Root Access.')

    elif command == 'removepass':
        if root:
            with open('SavedPasswords.txt', 'r') as f:
                all_pass_encrypt = f.readlines()
            all_pass = []
            for index in all_pass_encrypt:
                all_pass.append(decrypt(index))
            to_find = input('What is the label of the password that you want to remove. >>> ')
            i = 0
            for index in all_pass:
                if to_find == index:
                    all_pass.pop(i)
                    all_pass.pop(i)
                    all_pass.pop(i)
                    all_pass.pop(i)
                else:
                    i += 1
            with open('SavedPasswords.txt', 'w') as f:
                i = 0
                for index in all_pass:
                    i += 1
                    if len(all_pass) != i:
                        f.write(encrypt(index) + '\n')
                    else:
                        f.write(encrypt(index))
            print('Account Removed!')
        else:
            print('No Root Access')

    elif command == 'genpass':
        length = int(input('How Long? >>> '))
        all_char = string.ascii_letters + string.digits + string.punctuation
        new_pass = []
        for i in range(length):
            ran_char = random.choice(all_char)
            new_pass.append(ran_char)
        final_pass = "".join(new_pass)
        print(f'You new password is {final_pass}.')
        pyperclip.copy(final_pass)
        print('It has been copied to your clipboard')
        if root:
            y_or_n = input('Do you wish to add a new account with the password?(y/n) >>> ').lower()
            if y_or_n == 'y' or y_or_n == 'yes':
                new_label = input('What label do you want for this account? >>> ')
                new_user_email = input('What is the username/email/phone-number for this account? >>> ')
                y_or_n = input(f'Is this correct?(y/n)\n{new_label}\n{new_user_email}\n{final_pass}\n>>> ')
                if y_or_n == 'y' or y_or_n == 'yes':
                    with open('SavedPasswords.txt', 'r') as f:
                        saved_passes = f.readlines()
                    if len(saved_passes) == 0:
                        with open('SavedPasswords.txt', 'a') as f:
                            f.write(encrypt(new_label))
                            f.write('\n' + encrypt(new_user_email))
                            f.write('\n' + encrypt(final_pass))
                            f.write('\n' + encrypt('|'))
                            print('Account added.')
                    else:
                        with open('SavedPasswords.txt', 'a') as f:
                            f.write('\n' + encrypt(new_label))
                            f.write('\n' + encrypt(new_user_email))
                            f.write('\n' + encrypt(final_pass))
                            f.write('\n' + encrypt('|'))
                            print('Account added.')
                else:
                    print('Account not added.')
        else:
            continue

    elif command == 'newroot':
        if root:
            new_root_pass = input('Enter the new root password that you want. >>> ')
            main_data_encrypt[0] = encrypt(new_root_pass)
            main_data[0] = new_root_pass
            with open('MainData.txt', 'w') as f:
                for index in main_data_encrypt:
                    f.write(index)
                print(f'Your new root password is {new_root_pass}.')
        else:
            print('No Root Access')

    elif command == 'root':
        user_attempt = input('What is the root password? >>> ')
        if user_attempt == main_data[0]:
            print('Root Enabled.')
            root = True
        else:
            print('Password Incorrect')

    elif command == 'exit':
        print('Goodbye!')
        running = False

    elif command == 'webbrowser':
        print('Your default web browser had been opened')
        webbrowser.open('https://google.com')

    elif command == 'resetmaindata':
        if root:
            are_you_sure = input('Retype the command with proper capitilization.(ResetMainData) >>> ')
            if are_you_sure == 'ResetMainData':
                reset_maindata()
        else:
            print('No Root Access')

    elif command == 'resetsavedpasswords':
        if root:
            are_you_sure = input('Retype the command with proper capitilization.(ResetSavedPasswords) >>> ')
            if are_you_sure == 'ResetSavedPasswords':
                reset_passwords()
        else:
            print('No Root Access')

    elif command == 'dataset':
        file = input('Do you have a data file with all of the numbers on separate lines? (y/n) >>> ').lower()
        if file == 'y' or file == 'yes':
            file_name = input('What is the name of the file? >>> ')
            file_extension = input('What is the file extension? (Should be txt) >>> ')
            file_directory = input('Where is the file located? (All Slashes Need to Be included)(Optional) >>> ')
            with open(f'{file_directory}{file_name}.{file_extension}', 'r') as f:
                dataset = f.readlines()
            dataset_temp = []
            for num in dataset:
                dataset_temp.append(int(num.strip()))
            dataset = dataset_temp
            dataset.sort()
            print(f'The sum is {sum(dataset)}')
            print(f'The mean is {statistics.mean(dataset)}')
            print(f'The median is {statistics.median(dataset)}')
            print(f'The mode is {statistics.mode(dataset)}')
            print(f'The Standard Deviation is {statistics.stdev(dataset)}')
            print(f'Your sorted list is {dataset}')
        else:
            data = []
            amount = int(input('How many numbers do you have? >>> '))
            for i in range(0, amount):
                number_to_add = input(f'Number #{i + 1} >>> ')
                if number_to_add.lower() == 'q' or number_to_add.lower() == 'quit':
                    print('Stopped')
                    break
                else:
                    data.append(float(number_to_add))
            if number_to_add.lower() == 'q' or number_to_add.lower() == 'quit':
                pass
            else:
                data.sort()
                print(f'The sum is {sum(data)}')
                print(f'The mean is {statistics.mean(data)}')
                print(f'The median is {statistics.median(data)}')
                print(f'The mode is {statistics.mode(data)}')
                print(f'The Standard Deviation is {statistics.stdev(data)}')
                print(f'Your sorted list is {data}')

    elif command == 'createfile':
        if root:
            file_name = input('What do you want to name the file? >>> ')
            file_extension = input('What do you want the file extension to be? >>> ')
            file_directory = input('Where do you want the file to be? (All Slashes Need to Be included)(Optional) >>> ')
            open(f'{file_directory}{file_name}.{file_extension}', 'w')
            print(f'File {file_name}.{file_extension} created.')
        else:
            print('No Root Access')

    elif command == 'terminal':
        command = input('Please Type Your Linux Command. >>> ')
        os.system(f"gnome-terminal -H -x {command}")
    elif command == 'thank_you!' or command == 'thank_you' or command == 'thank you' or command == 'thank you!' or command == 'thanks' or command == 'thanks!':
        print('Your Welcome!')

    elif command == 'graph':
        how_many_cords = ''
        while isinstance(how_many_cords, str):
            try:
                how_many_cords = int(input('How many points do you have? >>> '))
            except ValueError:
                print('You need to input a whole number.')

        x = []
        y = []
        print('Enter your x values in order.')
        for i in range(0, how_many_cords):
            x_value = input(f'x value #{i} >>> ')
            x.append(x_value)
        print('Enter your y values in order.')
        for i in range(0, how_many_cords):
            y_value = input(f'y value #{i} >>> ')
            y.append(y_value)
        plt.plot(x, y, color='red', linestyle='solid', linewidth=2,
                 marker='o', markersize=6,
                 markerfacecolor='blue', markeredgecolor='blue')
        plt.grid()
        plt.show()

    elif command == '':
        print("You're meant to input a command. Type help for a list of commands.")

    else:
        print('Not Understood, Please Try Again.')
