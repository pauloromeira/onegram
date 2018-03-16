from hashlib import md5


def hash_id(string):
    return md5(string.encode()).hexdigest()
