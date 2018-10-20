
__ALL__ = [
    'encrypt_string',
    'validate_string'
]


def encrypt_string(text_string):
    generated = bcrypt.generate_password_hash(password=text_string)
    print(generated)
    return generated

def validate_string(hash_value, text_string):
    response = bcrypt.check_password_hash(hash_value, text_string)
    print(response)
    return response