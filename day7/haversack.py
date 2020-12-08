import re

BAG_MATCH_REGEX = re.compile('^(P<bag>.*) bags contain ((P<contents>\d+ .*) bag(s)?(,|.))+$')

class Bag():
    def __init__(self, line):
        split = line.split(' bags contain ')
        self.bag_type = split[0]
        self.contains = self.parse_contains(split[1])

    def parse_contains(self, contained):
        print(contained)
        if contained == 'no other bags.':
            return {}

        contains = {}
        split = contained.split(', ')
        for bag in split:
            bag = bag.split(' ')
            quantity = int(bag[0])
            kind = bag[1] + ' ' + bag[2]
            contains[kind] = quantity

        return contains

    def __repr__(self):
        ss = f'bag type: {self.bag_type}\n'
        ss += f'contains:\n'
        for key in self.contains.keys():
            quantity = self.contains[key]
            ss += f'{quantity} {key}\n'

        return ss

def split_to_map(line):
    if line == 'no other bags.':
        return {}

    contents = {}
    split = line.split(', ')
    for bag in split:
        bag = bag.split(' ')
        quantity = int(bag[0])
        kind = bag[1] + ' ' + bag[2]
        contents[kind] = quantity

    return contents

def dfs(from_here, to, bags):
    contained = bags.get(from_here)
    if not contained:
        return 0

    for key in contained:
        if key == to:
            return 1
        if dfs(key, to, bags):
            return 1

    return 0

def bfs(target, bags):
    num_bags_contained = 0
    queue = []

    queue.append((target, 1))

    while len(queue):
        bag, quantity = queue.pop(0)
        for key in bags[bag]:
            num = bags[bag][key]
            queue.append((key, num * quantity))
        num_bags_contained += quantity
         
    return num_bags_contained - 1

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    bags = {}
    with open(args.in_file, 'r') as ff:
        for line in ff:
            line = line.rstrip().split(' bags contain ')
            bag_type = line[0]
            bags[bag_type] = split_to_map(line[1])

    num_routes = 0
    for bag in bags:
        num_routes += dfs(bag, 'shiny gold', bags)

    num_bags_contained = bfs('shiny gold', bags)
    print(num_routes)
    print(num_bags_contained)
