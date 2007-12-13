import random

def random_data(points=50, maximum=100):
    return [random.random() * maximum for a in xrange(points)]

