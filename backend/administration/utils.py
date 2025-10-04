def generate_valid_schema_name(company_name):
    """
    Generate a valid PostgreSQL schema name
    """
    import re
    import random
    import string
    
    # Clean the name - only alphanumeric and underscores
    schema_name = re.sub(r'[^a-zA-Z0-9_]', '', company_name.lower().replace(' ', '_'))
    
    # Ensure it starts with a letter
    if not schema_name or not schema_name[0].isalpha():
        schema_name = 'cmp_' + schema_name
    
    # Ensure it's not empty and has valid length
    if not schema_name:
        schema_name = 'company_' + ''.join(random.choices(string.ascii_lowercase, k=8))
    
    # Truncate to 63 characters (PostgreSQL limit)
    schema_name = schema_name[:63]
    
    return schema_name