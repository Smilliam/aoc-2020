
class CharSet():
    def __init__(self, string):
        self._chars = [0 for x in range(0, 26)]
        self.add_answers(string)

    def add_answers(self, answers):
        for ch in answers:
            letter_idx = ord(ch) - 97
            self._chars[letter_idx] ^= 1

    def num_unique_answers(self):
        return sum(self._chars)

    def intersect(self, other_list):
        return [x for x in map(lambda a, b: a & b, self._chars, other_list)]


def find_intersection(sets):
    blank = [1 for x in range(0, 26)]
    for char_set in sets:
        blank = char_set.intersect(blank)

    return blank

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args();

    total_group_intersection = 0
    with open(args.in_file, 'r') as ff:
        group_sets = []  # CharSets for one entire group
        for line in ff:
            line = line.rstrip()
            if line == '':
#                import pdb; pdb.set_trace()
                total_group_intersection += sum(find_intersection(group_sets))
                group_sets = []
            else:
                group_sets.append(CharSet(line))

        if len(group_sets): 
            total_group_intersection += sum(find_intersection(group_sets))

    print(total_group_intersection)
