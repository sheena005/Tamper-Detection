import matplotlib.pyplot as plt

def visualize_tree(tree):

    # show only first few levels
    max_levels = min(4, len(tree))

    fig, ax = plt.subplots(figsize=(8,4))

    for level in range(max_levels):

        nodes = tree[level][:6]   # show only first 6 nodes

        y = max_levels - level

        for i, node in enumerate(nodes):

            ax.text(
                i,
                y,
                node[:6],
                ha="center",
                bbox=dict(boxstyle="round", fc="lightblue")
            )

    ax.set_title("Merkle Tree (Top Levels)")
    ax.axis("off")

    return fig