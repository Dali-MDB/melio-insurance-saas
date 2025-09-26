import random

def generate_policy_number(length=4,repeat=3):
    digs = '0123456789'
    rslt = ''
    for _ in range(repeat):
        rslt += ''.join(random.choice(digs) for i in range(length))
        rslt +='-'
    return rslt[:-2]    #to get rid of the last -


