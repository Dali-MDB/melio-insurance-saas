import random

def generate_claim_number(length=4,repeat=3):
    digs = '0123456789'
    rslt = ''
    for _ in range(repeat):
        rslt += ''.join(random.choice(digs) for i in range(length))
        rslt +='-'
    return 'CLM-'+rslt[:-2]    #to get rid of the last -

import uuid
def is_valid_uuid4(value):
    try:
        potential_uuid = uuid.UUID(str(value)) 
        return potential_uuid.version == 4
    except ValueError:
        return False