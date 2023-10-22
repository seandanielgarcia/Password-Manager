from cryptography.fernet import Fernet
import random
import string
from decouple import config



def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

def setup_fernet(masterPwd):
    key = load_key() + masterPwd.encode('utf-8')
    return Fernet(key)

def view_passwords(fer):
    with open('passwords.txt', 'r') as f:
        lines = f.readlines()

    if not lines:
        print("There are no passwords to view.")
    else:
        for line in lines:
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())

def add_password(fer):
    name = input('Account name: ')
    pwd = input('Account password: ')

    try:
        with open('passwords.txt', 'a') as f:
            f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
        print("Password added successfully.")
    except Exception as e:
        print("An error occurred while adding the password:", str(e))

def delete_password(fer):
    nameDelete = input('Account name: ')
    found = False

    with open('passwords.txt', 'r') as f:
        lines = f.readlines()

    with open('passwords.txt', 'w') as f:
        for line in lines:
            data = line.rstrip()
            user, passw = data.split("|")
            if user == nameDelete:
                found = True
                print(f"Are you sure you'd like to delete the password for {user}?")
            else:
                f.write(line)

    if not found:
        print(f"Password entry for '{nameDelete}' not found.")
    elif input("Type 'yes' to confirm deletion: ").lower() == "yes":
        print("Password deleted successfully.")
    else:
        print("Password deletion canceled.")

def generate_password(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    gen_pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(gen_pwd) < min_length:
        new_char = random.choice(characters)
        gen_pwd += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special

    return gen_pwd

def add_generated_password(fer, gen_pwd):
    name = input('Account name: ')

    try:
        with open('passwords.txt', 'a') as f:
            f.write(name + "|" + fer.encrypt(gen_pwd.encode()).decode() + "\n")
        print("Password added successfully.")
    except Exception as e:
        print("An error occurred while adding the password:", str(e))

def run_password_manager(masterPwd):
    fer = setup_fernet(masterPwd)

    while True:
        mode = input("Would you like to view existing passwords, add a new password, generate password, or delete a password? (view, add, delete, generate, press 'q' to quit): ").lower()
        if mode == "q":
            break

        if mode == "view":
            view_passwords(fer)
        elif mode == "add":
            add_password(fer)
        elif mode == "delete":
            delete_password(fer)
        elif mode == "generate":
            min_length = int(input("How long would you like for the password to be: "))
            has_number = input("Would you like the password to include numbers (y/n): ").lower() == "y"
            has_special = input("Would you like the password to include special characters (y/n): ").lower() == "y"
            gen_pwd = generate_password(min_length, has_number, has_special)
            print("The generated password is", gen_pwd)

            while True:
                add_generated_password_option = input("Would you like to add this password to your saved passwords (y/n): ")
                if add_generated_password_option == "y":
                    add_generated_password(fer, gen_pwd)
                    break
                elif add_generated_password_option == "n":
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

def runProgram():
    
    passwordChances = 5
    masterPwd = "CodingIsFun"
    while passwordChances > 0:
        masterPassword = input("What is the master password? ")

        if masterPassword == masterPwd:
            print("Correct master password. You can now run the password manager.")
            run_password_manager(masterPwd)
            break

        else:
            passwordChances -= 1
            print(f"Incorrect password. {passwordChances} attempts left.")

    if passwordChances == 0:
        print("Out of password attempts. Exiting program.")

runProgram()
