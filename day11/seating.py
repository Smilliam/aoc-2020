import copy
from pprint import pprint

def check_neighbors(grid, row, col):
    occupied = 0
    empty = 0
    for x in range(row-1, row+2):
        if x < 0 or x >= len(grid):
            continue
        for y in range(col-1, col+2):
            if y < 0 or y >= len(grid[0]):
                continue
            if x == row and y == col:
                pass
            elif grid[x][y] == '#':
                occupied += 1
            else:
                empty += 1

    return apply_rules(grid[row][col], occupied, empty)

def apply_rules(state, occupied, empty):
    if state == 'L' and occupied == 0:
        return ('#', True)
    elif state == '#' and occupied >= 4:
        return ('L', True)
    else:
        return (state, False)

def check_los(grid, row, col):
    empty = 0
    occupied = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue

            next_x = row + x
            next_y = col + y
            while 0 <= next_x < len(grid) and 0 <= next_y < len(grid[0]) \
                  and grid[next_x][next_y] == '.':
                next_x += x
                next_y += y

            if 0 <= next_x < len(grid) and 0 <= next_y < len(grid[0]):
                if grid[next_x][next_y] == '#':
                    occupied += 1
                else:
                    empty += 1

    return apply_rules2(grid[row][col], occupied, empty)


def apply_rules2(state, occupied, empty):
    if state == 'L' and occupied == 0:
        return ('#', True)
    elif state == '#' and occupied >= 5:
        return ('L', True)
    else:
        return (state, False)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file

    seats = []
    with open(in_file, 'r') as ff:
        for line in ff:
            seats.append(line.rstrip())

    print(f'{len(seats)} rows')
    print(f'{len(seats[0])} cols')
    next_state = []
    changed = True
    while changed:
#        import pdb; pdb.set_trace()
        changed = False
        for ii in range(len(seats)):
            row = seats[ii]
            next_row = []
            for jj in range(len(row)):
                state, did_change = check_los(seats, ii, jj)
                next_row.append(state)
                changed |= did_change
            next_state.append(next_row)

        seats = next_state[:]
        next_state = []
#        pprint(seats)

    count = 0
    for row in seats:
        for col in row:
            if col == '#':
                count += 1

    print(count)
