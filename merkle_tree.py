#   Tree depth y = 2^x
#   y = number of leaves
#   x = tree depth
#   x = log_2(y)
import math

from cryptography import calculate_hash
from transaction import Transaction


class TreeNode:
    def __init__(self, value: int, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


def compute_tree_depth(number_of_leaves: int) -> int:
    return math.ceil(math.log2(number_of_leaves))


def build_merkle_tree(transactions: [Transaction]) -> TreeNode:
    # print(transactions)
    bottom = [TreeNode(calculate_hash(str(t))) for t in transactions]
    bottom = fill_leaves(bottom)
    tree_depth = compute_tree_depth(len(bottom))

    for i in range(0, tree_depth):
        num_nodes = 2 ** (tree_depth - i)
        top = []
        for j in range(0, num_nodes, 2):
            child_node_0 = bottom[j]
            child_node_1 = bottom[j + 1]
            new_node = TreeNode(
                value=calculate_hash(f"{child_node_0.value}{child_node_1.value}"),
                left_child=child_node_0,
                right_child=child_node_1
            )
            top.append(new_node)
        bottom = top
    return top[0]


def is_power_of_2(number_of_leaves: int) -> bool:
    return math.log2(number_of_leaves).is_integer()


def fill_leaves(nodes):
    number_of_leaves = len(nodes)
    if is_power_of_2(number_of_leaves):
        return nodes
    filled_number_of_leaves = 2 ** compute_tree_depth(number_of_leaves)
    if number_of_leaves % 2 == 0:
        for i in range(number_of_leaves, filled_number_of_leaves, 2):
            nodes = nodes + [nodes[-2], nodes[-1]]
    else:
        for i in range(number_of_leaves, filled_number_of_leaves):
            nodes.append(nodes[-1])
    return nodes
