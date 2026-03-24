import hashlib

def build_merkle_tree(hashes):

    tree = []
    tree.append(hashes)

    while len(hashes) > 1:

        new_level = []

        for i in range(0, len(hashes), 2):

            left = hashes[i]

            if i+1 < len(hashes):
                right = hashes[i+1]
            else:
                right = left

            combined = hashlib.sha256((left+right).encode()).hexdigest()

            new_level.append(combined)

        hashes = new_level
        tree.append(hashes)

    return tree


def get_merkle_root(tree):

    return tree[-1][0]