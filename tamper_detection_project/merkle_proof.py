def generate_merkle_proof(tree, index):

    proof = []

    for level in tree[:-1]:

        if index % 2 == 0:

            sibling = index + 1

        else:

            sibling = index - 1

        if sibling < len(level):
            proof.append(level[sibling])

        index = index // 2

    return proof