import random
import string

def mock_post():
    """Generate some random post text."""
    count = random.randint(70, 256)
    return ''.join([random.choice(string.letters) for i in xrange(count)])

