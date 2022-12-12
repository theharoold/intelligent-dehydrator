import hashlib

SALT = 'salted'
PASSWORDS_FILE = 'passwords.txt'

def authenticate(password, password_file):
    # read the password file
    with open(password_file, 'r') as f:
        for line in f:
            # hash the user's password with the salt from the password file
            salted_password = hashlib.sha256((SALT + password).encode()).hexdigest()

            line = line.strip()

            # check if the salted password is equal to the password in the file
            if salted_password == line:
                # the user has successfully authenticated
                return True

    # the user has not authenticated
    return False

def addNewPassword(password_file, password):
    # Open the file in write mode
    f = open(password_file, 'a')

    hashedPassword = hashlib.sha256((SALT + password).encode())

    # Write some text to the file
    f.write(hashedPassword.hexdigest() + '\n')

    # Close the file
    f.close()