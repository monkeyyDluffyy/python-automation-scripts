import random
import string

def generate_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%&*"

    password_chars= []
    password_chars.append(random.choice(uppercase))
    password_chars.append(random.choice(lowercase))

    password_chars.append(random.choice(digits))
    password_chars.append(random.choice(digits))

    password_chars.append(random.choice(special))

    all_chars = uppercase + lowercase + digits + special

    while len(password_chars) < 16:
        char = random.choice(all_chars)

        if char not in password_chars:
            password_chars.append(char)

    random.shuffle(password_chars)

    password = ''.join(password_chars)

    return password


print("Generated Password:", generate_password())