"""
Predict the value of input[index] from the values of input[:index]
"""
def predict(input,index=None):
    if index is None:
        return None

    """
    Initialize with research results for patterns of length 1
    """
    pattern_length = 1
    # The element that should be compared to the rest of the input
    controlled_element = input[index-pattern_length]
    end_pattern_indices = set()
    # Patterns matching the end of the input
    # Only the index of the end of every matching pattern is stored
    tmp_end_pattern_indices = {\
            # i is the matching character, i+pattern_length-1
            # is then the index of the end of the pattern
            i + pattern_length - 1\
            for i in range(index-pattern_length)\
            if input[i] is controlled_element\
        }

    """
    While there are matching patterns, try a higher length.
    """
    while len(tmp_end_pattern_indices):
        end_pattern_indices.append(tmp_end_pattern_indices)
        pattern_length += 1
        # Control the next character (from right to left)
        # of the pattern to match
        controlled_element = input[index-pattern_length]
        tmp_end_pattern_indices = {\
                i + pattern_length - 1\
                for i in range(index-pattern_length)\
                if input[i] is controlled_element\
            } & end_pattern_indices

    """
    In the end, return a prediction based on the last batch
    of matching patterns.
    """
    if len(end_pattern_indices):
        # Maximum length for which a pattern was found
        max_pattern_length = len(end_pattern_indices)
        # Multiply by alpha
        chosen_pattern_length =\
                min(max_pattern_length-1,\
                    int(max_pattern_length*self.alpha))
        # Available predictions for this pattern length
        predictions = [self.string[x+1] for x in end_pattern_indices[index]]
        # Return the most frequent one
        return max(set(predictions),key=predictions.count)

    # None is the special value to say "unable to predict"
    return None
