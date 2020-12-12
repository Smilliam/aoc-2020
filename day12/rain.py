import logging
from enum import Enum

logging.basicConfig()
logger = logging.getLogger('rain')
logger.setLevel('INFO')

class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    F = 100
    R = 1000
    L = 2000

class Quadrant(Enum):
    NE = 0
    SE = 1
    SW = 2
    NW = 3
    ORIGIN = 4

class Waypoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._set_quadrant()

    def step(self, instruction, val):
#        logger.debug(f'{instruction}: {val}')
        if instruction == Direction.L or instruction == Direction.R:
            self.rotate(instruction, val)
        else:
            self.move(instruction, val)

    def move(self, direction, distance):
        if direction == Direction.F:
            self.move(self.facing, distance)
        if direction == Direction.N:
            self.y = self.y + distance
        if direction == Direction.S:
            self.y = self.y - distance
        if direction == Direction.E:
            self.x = self.x + distance
        if direction == Direction.W:
            self.x = self.x - distance

        if self.x == 0 or self.y == 0:
            logger.debug(f'!!!!!  {self.x} {self.y}  !!!!!')
        self._set_quadrant()
        logger.debug(f'New location: {self.x}, {self.y}')

    def rotate(self, direction, angle):
        num_turns = angle / 90
        while num_turns:
            if direction == Direction.L:
                self.quadrant = Quadrant((self.quadrant.value - 1) % 4)
            else:
                self.quadrant = Quadrant((self.quadrant.value + 1) % 4)
            tmp = self.x
            self.x = self.y
            self.y = tmp
            num_turns -= 1

        self._set_position()
        logger.debug(f'{self.quadrant}: {self.x}, {self.y}')

    def _set_quadrant(self):
        if self.x > 0 and self.y > 0:
            self.quadrant = Quadrant.NE
        elif self.x > 0 and self.y < 0:
            self.quadrant = Quadrant.SE
        elif self.x < 0 and self.y < 0:
            self.quadrant = Quadrant.SW
        elif self.x < 0 and self.y > 0:
            self.quadrant = Quadrant.NW
#        else:
#            self.quadrant = Quadrant.ORIGIN

    def _set_position(self):
        if self.quadrant == Quadrant.NE:
            self.x = abs(self.x)
            self.y = abs(self.y)
        if self.quadrant == Quadrant.SE:
            self.x = abs(self.x)
            self.y = -abs(self.y)
        if self.quadrant == Quadrant.SW:
            self.x = -abs(self.x)
            self.y = -abs(self.y)
        if self.quadrant == Quadrant.NW:
            self.x = -abs(self.x)
            self.y = abs(self.y)

    def manhattan(self):
        return abs(self.x) + abs(self.y)

class Boat(Waypoint):
    def __init__(self, facing, x, y):
        self.facing = facing
        Waypoint.__init__(self, x, y)

    def rotate(self, direction, angle):
#        logger.debug(f'Cur facing: {self.facing}. Incoming rotation {direction}, {angle}')
        if direction == Direction.L:
            self.facing = Direction((self.facing.value - (angle / 90)) % 4)
        else:
            self.facing = Direction((self.facing.value + (angle / 90)) % 4)
#        logger.debug(f'Facing is now {self.facing}')


class Ship(Waypoint):
    def __init__(self, facing):
        self.waypoint = Waypoint(10, 1)
        self.x = 0
        self.y = 0

    def step(self, instruction, val):
        logger.debug(f'({instruction}, {val})')
        if instruction == Direction.F:
            self.x += self.waypoint.x * val
            self.y += self.waypoint.y * val
            logger.debug(f'Ship: {self.x}, {self.y}')
        else:
            self.waypoint.step(instruction, val)
            logger.debug(f'WP: {self.waypoint.x}, {self.waypoint.y}')


def ch_to_direction(ch):
    if ch == 'N':
        return Direction.N
    if ch == 'E':
        return Direction.E
    if ch == 'S':
        return Direction.S
    if ch == 'W':
        return Direction.W
    if ch == 'F':
        return Direction.F
    if ch == 'R':
        return Direction.R
    if ch == 'L':
        return Direction.L

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file

    navigation = []
    with open(in_file, 'r') as ff:
        for line in ff:
            line = line.rstrip()
            direction = ch_to_direction(line[0])
            navigation.append((direction, int(line[1:])))

    boat = Boat(Direction.E, 0, 0)

    for ins, val in navigation:
        boat.step(ins, val)

    print(boat.manhattan())

    ship = Ship(Direction.E)
    for ins, val in navigation:
        ship.step(ins, val)

    print(ship.manhattan())
