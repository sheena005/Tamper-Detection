import hashlib
from blake3 import blake3

def select_hash(file_type):

    if "video" in file_type:
        return "sha3_256"

    elif "audio" in file_type:
        return "blake3"

    elif "image" in file_type:
        return "sha256"

    else:
        return "sha256"


def hash_chunk(chunk, algo):

    if algo == "blake3":
        return blake3(chunk).hexdigest()

    h = hashlib.new(algo)
    h.update(chunk)

    return h.hexdigest()