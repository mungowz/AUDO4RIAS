class SearchTree:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

    def insert(self, val):
        if not self.val:
            self.val = val
            return
        if self.val == val:
            return
        if val < self.val:
            if self.left:
                self.left.insert(val)
                return
            self.left = SearchTree(val)
            return
        if self.right:
            self.right.insert(val)
            return
        self.right = SearchTree(val)

    def exists(self, val):
        if val == self.val:
            return True
        if val < self.val:
            if self.left == None:
                return False
            return self.left.exists(val)
        if self.right == None:
            return False
        return self.right.exists(val)
