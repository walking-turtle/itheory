def predict(l):
    pattern_length = 1
    controlled_element = l[-pattern_length]
    end_pattern_indices = set()
    tmp_end_pattern_indices = { i + pattern_length - 1 for i in range(len(l)-pattern_length) if l[i] is controlled_element }
    print(tmp_end_pattern_indices)
    while len(tmp_end_pattern_indices):
        end_pattern_indices = tmp_end_pattern_indices
        pattern_length += 1
        controlled_element = l[-pattern_length]
        tmp_end_pattern_indices = { i + pattern_length - 1 for i in range(len(l)-pattern_length) if l[i] is controlled_element } \
                & end_pattern_indices
        print(tmp_end_pattern_indices)
    return l[max(end_pattern_indices)+1]
