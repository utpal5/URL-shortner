import random
import string
import re

def generate_short_code(length=6):
    """Generate a random alphanumeric short code of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def is_valid_url(url):
    """Basic URL validation using regex."""
    regex = re.compile(
        r'^(https?://)?'  # http:// or https:// (optional)
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # domain
        r'(:\d+)?'  # optional port
        r'(/[\w./?%&=-]*)?$'  # path and query string
    )
    return re.match(regex, url) is not None
