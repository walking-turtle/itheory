class Predictions(TreeData):
    """
    If `sequence` is "abcde" and `prediction` is "f", add
    `e -> d -> c -> b -> a -> f' to the tree.
    """
    def add(self,sequence,prediction):
        node = self.tree
        for x in reversed(sequence):
            if x not in node:
                node[x] = dict()
            node = node[x]
        node['__'] = prediction

    """
    Get a prediction for the next character of `sequence'
    """
    def get(self,sequence):
        node = self.tree
        # Try to find the longest pattern matching the end
        # of `sequence` by walking as deep as possible into
        # the tree.
        for x in sequence[::-1]:
            if x not in node:
                break
            node = node[x]
        # If there is a prediction at this point in the tree,
        # return it.
        return node.get('__',None)

    """
    Convert substrings to a prediction tree. To predict the
    character following "abcde", in the tree there will be
    an entry `e -> d -> c -> b -> a -> prediction'.
    """
    @classmethod
    def from_substrings(cls,substrings):
        # Create predictions object
        self = cls(cache = substrings.cache)
        # `path' will contain the current path during iteration
        path = list()
        # `key' is the current character in the tree,
        # `node' contains the children and the counter of the
        # current branch
        for key,node,depth in substrings.iteritems():
            # Remember the path we are currently looking at
            path[depth] = key
            # Children: every key in `node` that has a counter.
            children = list(filter(lambda x: x!='__' and '__' in node[x],\
                    node))
            # Choose the best child, i.e. the most frequent next
            # character.
            if children:
                maximum, best_child = 0, 'xxx'
                for child in children:
                    if node[child]['__'] > maximum:
                        best_child = child
                        maximum = node[child]['__']
                # Add the best child as a prediction
                self.add(path[:depth+1], best_child)
        return self
