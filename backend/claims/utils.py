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
    


def is_valid_status_transition(current_status, new_status):
    allowed_transitions = {
        'reported': ['assigned', 'denied'],
        'assigned': ['under_review', 'documents_requested', 'denied'],
        'under_review': ['investigation', 'documents_requested'],
        'investigation': ['waiting_approval', 'documents_requested'],
        'documents_requested': ['investigation', 'waiting_approval'],
        'waiting_approval': ['approved', 'denied'],
        'approved': ['payment_processing'],
        'payment_processing': ['paid'],
        'paid': ['closed'],
        'denied': ['closed'],
    }
    
    return new_status in allowed_transitions.get(current_status, [])