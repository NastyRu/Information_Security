LEFT = '1'
RIGHT = '0'


class Leaf():
    def __init__(self, data, freq):
        self.data = data
        self.freq = freq
        self.code = ''

    def update_code(self, update):
        self.code = update + self.code


class Node():
    def __init__(self, left, right, freq):
        self.freq = freq
        self.left = left
        self.right = right
        self.code = ''
        self.left.update_code(LEFT)
        self.right.update_code(RIGHT)

    def update_code(self, update):
        self.code = update + self.code
        self.left.update_code(update)
        self.right.update_code(update)


def buildTree(byte_frequencies):
    tree = [Leaf(bf[0], bf[1]) for bf in byte_frequencies]

    leaves = []
    while len(tree) > 1:
        left, right = tree[:2]
        if type(left) is Leaf:
            leaves.append(left)
        if type(right) is Leaf:
            leaves.append(right)
        tree = tree[2:]
        node = Node(left, right, left.freq + right.freq)
        tree.append(node)
        tree = sorted(tree, key=lambda node: node.freq)

    return leaves, tree[0]
