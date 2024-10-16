import random
import string

def generate_random_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(8))
    return code