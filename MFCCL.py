import random
import pyperclip
import cryptography
from cryptography.fernet import Fernet
import string

running = True
root = False
root_login = True

# Test

def load_key():
    with open('key.key', 'rb') as file:
        key = file.read()
    return key


key = load_key()
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
(h)elp > Shows a list of useful commands.
(q)uit > Stops the program.
*showpass > Shows all current passwords that are saved.     
*newpass > Adds a new password.
*removepass > Removes a password.
genpass > Generates a random secure password from 8-16 characters long.
*newroot > Allows the user to change the root password.
root > Allows the user to retry root login.
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

    else:
        print('Not Understood, Please Try Again.')
