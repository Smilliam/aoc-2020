from intervaltree import Interval, IntervalTree
from pprint import pprint

class Ticketer():
    def __init__(self):
        self.interval_tree = IntervalTree()

    def add_rule(self, line):
        split = line.rstrip().split(': ')
        rule = split[0]
        intervals = split[1].split(' or ')
        for interval in intervals:
#            print(f'Adding {interval} for {rule}')
            interval = interval.split('-')
            start = int(interval[0])
            end = int(interval[1])
            self.interval_tree[start:end+1] = rule

    def search(self, needle):
        return self.interval_tree[needle]

    def exists(self, needle):
        return self.interval_tree.overlaps(needle)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file

    ticketer = Ticketer()
    with open(in_file, 'r') as ff:
        line = ff.readline()
        while line != '\n':
            ticketer.add_rule(line)
            line = ff.readline()

        ff.readline() # your ticket:

        my_ticket = [int(val) for val in ff.readline().split(',')]

        ff.readline() # \n
        ff.readline() # nearby tickets:

        total_errors = 0
        valid_tickets = []
        line = ff.readline()
        while line != '':
            vals = [int(val) for val in line.split(',')]
            error = False
            for val in vals:
                found = ticketer.search(val)
                if not found:
                    error = True
                    total_errors += val

            if not error:
                valid_tickets.append(vals)

            error = False
            line = ff.readline()

        print(f'ticket scanning error rate: {total_errors}')

        fields = []
        num_fields = len(my_ticket)

        for ticket in valid_tickets:
            for i, val in enumerate(ticket):
                val = int(val)
                intervals = ticketer.search(val)
                if len(intervals) == 0:
                    import pdb; pdb.set_trace()
                if len(fields) == i:
                    interval_set = set()
                    for interval in intervals:
                        interval_set.add(interval.data)

                    fields.append(interval_set)
                else:
                    interval_set = set()
                    for interval in intervals:
                        interval_set.add(interval.data)
                    fields[i] = fields[i].intersection(interval_set)

        fields_to_solve = len(fields)
        solved_fields = set()
        i = 0
        while len(solved_fields) != fields_to_solve:
            if i == len(fields):
                i = 0
            field = fields[i]

            # If we only have one possibility for this
            # field, it *must* be that one, so purge it
            # from all the rest
            if len(field) == 1:
                solved_fields.add(list(field)[0])
                for j in range(0, len(fields)):
                    if i != j:
                       other = fields[j]
                       fields[j] = fields[j].difference(field)

            i += 1

        fields = [s.pop() for s in fields]
        print(f'{fields}')

        product = 1
        for i, field in enumerate(fields):
            if 'departure' in field:
                product *= my_ticket[i]

        print(f'departure field product: {product}')
