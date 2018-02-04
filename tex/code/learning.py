"""
Tree counting substrings shorter than `cache' in every text that
was read before.
"""
class SubStrings(TreeData):
    """
    Add a substring to the tree. If the substring is "abcdef", in
    the tree it will be `a -> b -> c -> d -> e -> f -> (counter)'
    """
    def add(self,sequence):
        node = self.tree
        # Walk in the tree to find or create the substring
        for x in sequence:
            # If need be, create the node
            if x not in node:
                node[x] = dict()
            node = node[x]
        # Increase the occurence counter of the substring
        node['__'] = node.get('__',0)+1

    """
    Parse data and count substrings of length <= `cache'.
    """
    def parseiter(self,data):
        last = len(data)
        # Walk the whole data
        for i in range(last):
            # Add each substring ending at `i' and shorter than
            # `cache'
            for j in range(min(self.cache,i)):
                self.add(data[i-j-1:i])
