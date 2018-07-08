"""
Based off of https://gist.github.com/ndarville/3452907

Two things are wrong with Django's default `SECRET_KEY` system:

1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`

This code
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`

The result is a random and safely hidden `SECRET_KEY`.
Make sure to exclude secret.txt from version control.

Usage in your settings.py file:
SECRET_KEY = get_secret('/etc/path/tosecret.txt')

If a file exists at the path, it will read the file contents
and use that as the secret.  If the file does not exist, then
it will generate a new secret and save it to the file, and return
the secret.

"""

def get_secret(location, num=50):
    try:
        SECRET_KEY = open(location).read().strip()
        return SECRET_KEY
    except IOError:
        SECRET_KEY = save_secret(location, generate_random_string(num))
        if SECRET_KEY:
            return SECRET_KEY
    return None


def generate_random_string(num):
    import random
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    chars = alpha + alpha.upper() + numbers
    return ''.join([random.SystemRandom().choice(chars) for _i in range(num)])


def save_secret(location, string):
    try:
        secret = file(location, 'w')
        secret.write(string)
        secret.close()
        return string
    except IOError:
        Exception(
            'Please create a {} file with random characters to generate your secret key!'.format(location))
