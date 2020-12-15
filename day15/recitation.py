def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    parser.add_argument('num_iter', type=int)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file
    iters = args.num_iter

    nums = []
    with open(in_file, 'r') as ff:
        line = ff.readline()
        line = line.split(',')
        nums = [int(x) for x in line]

    print(nums)

    lru_map = {}
    last = None
    next = None
    ii = 0
    while ii < iters:
        if len(nums):
            cur = nums.pop(0)
        elif not lru_map.get(last):
            cur = 0
        else:
            last_seen = lru_map[last]
            cur = ii - last_seen

        if last is not None:
            lru_map[last] = ii

        last = cur

        ii += 1

    print(last)
