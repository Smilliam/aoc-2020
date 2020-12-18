from pprint import pprint
import copy
import numpy as np

def check_neighbors(grid, row, col, alt):
    occupied = 0
    empty = 0
    for x in range(row-1, row+2):
        if x < 0 or x >= len(grid):
            continue
        for y in range(col-1, col+2):
            if y < 0 or y >= len(grid[0]):
                continue
            for z in range(alt-1, alt+2):
                if z < 0 or z >= len(grid[0][0]):
                    continue
                if x == row and y == col and z == alt:
                    pass
                elif grid[x][y][z] == '#':
                    occupied += 1
                else:
                    empty += 1
    return apply_rules(grid[row][col][alt], occupied, empty)

def check_neighbors_4d(grid, row, col, alt, t):
    occupied = 0
    empty = 0
    for x in range(row-1, row+2):
        if x < 0 or x >= len(grid):
            continue
        for y in range(col-1, col+2):
            if y < 0 or y >= len(grid[0]):
                continue
            for z in range(alt-1, alt+2):
                if z < 0 or z >= len(grid[0][0]):
                    continue
                for w in range(t-1, t+2):
                    if w < 0 or w >= len(grid[0][0][0]):
                        continue
                    if x == row and y == col and z == alt and w == t:
                        pass
                    elif grid[x][y][z][w] == '#':
                        occupied += 1
                    else:
                        empty += 1
    return apply_rules(grid[row][col][alt][t], occupied, empty)

def apply_rules(state, occupied, empty):
    if state == '#' and (occupied != 2 and occupied != 3):
        return ('.', True)
    elif state == '.' and occupied == 3:
        return ('#', True)
    else:
        return (state, False)

def print_grid(grid):
    num_z = len(grid[0][0])

    for z in range(num_z):
        print(f'z={z}')
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                print(col[z], end='')
            print()
        print()

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file

    grid = np.chararray((20,20,13,13), unicode=True)
    grid[:] = '.'

    with open(in_file, 'r') as ff:
        x = 6
        z = 6
        w = 6
        for line in ff:
            chars = list(line.rstrip())
            y = 6
            for ch in chars:
                grid[x][y][z][w] = ch
                y += 1
            x += 1

#    print_grid(grid)

    for i in range(6):
        next_state = np.chararray((20,20,13,13), unicode=True)
        next_state[:] = '.'
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                for z, alt in enumerate(col):
                    for w, t in enumerate(alt):
                        state, _ = check_neighbors_4d(grid, x, y, z, w)
                        next_state[x][y][z][w] = state
        grid = next_state[:]
        next_state = np.chararray((20,20,13,13), unicode=True)
        next_state[:] = '.'
#        print_grid(grid)

    num_active = 0
    for row in grid:
        for col in row:
            for z in col:
                for cube in z:
                    if cube == '#':
                        num_active += 1

    print(num_active)
