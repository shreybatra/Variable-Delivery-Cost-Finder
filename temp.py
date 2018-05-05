import pickle

class Tree:
    def __init__(self, node):
        self.left = None
        self.right = None
        self.data = node

root = None
pickle.dump(root, open("requests.pickle", "wb" ))