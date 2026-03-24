from hashing import hash_chunk

def detect_tampering(original_hashes, new_chunks, algo):

    new_hashes = []

    for chunk in new_chunks:
        new_hashes.append(hash_chunk(chunk, algo))

    modified = []

    # compare chunk hashes
    for i in range(min(len(original_hashes), len(new_hashes))):

        if original_hashes[i] != new_hashes[i]:
            modified.append(i)

    # if chunk count differs
    if len(original_hashes) != len(new_hashes):
        modified.append("File structure changed")

    return modified