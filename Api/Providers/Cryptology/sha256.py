from hashlib import sha256


async def encrypter(word):
    return sha256(word.encode('utf-8')).hexdigest()
