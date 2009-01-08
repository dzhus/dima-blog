from socket import gethostname

def at_dev():
    return gethostname() == 'blizzard'
