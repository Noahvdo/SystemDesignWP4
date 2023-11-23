def dynamic_loops(params, current=[], level=0):
    if level == len(params):
        print(current)  # Do something with the current combination
        return

    for i in range(params[level]):
        # If we're not at the last level, go deeper
        dynamic_loops(params, current + [i], level + 1)


# Example usage:
# 3 parameters with 2, 3, and 4 steps respectively
dynamic_loops([7, 4, 4])
