import random

def generate_code(length:int):
    digs = "0123456789"
    return ''.join(random.choice(digs) for _ in range(length))



