import re

MEM = re.compile('mem\[(?P<value>\d+)\]')
class Masker():
    def __init__(self):
        self._mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        self._positions = []

    def set_mask(self, mask):
        self._mask = mask

        # Only used for part 1
        self._positions = []
        for i, ch in enumerate(self._mask):
            if ch != 'X':
                self._positions.append((i, ch))

    def mask(self, to_mask):
        bin_str = list(f'{to_mask:b}'.zfill(36))
        for i, val in self._positions:
            bin_str[i] = val

        bin_str = "".join(bin_str)
        return int(bin_str, 2)

    def mask_addr(self, to_mask):
        bin_str = list(f'{to_mask:b}'.zfill(36))

        for i, ch in enumerate(self._mask):
            if ch == '1' or ch == 'X':
                bin_str[i] = ch

        addr_list = []
        self._generate_addrs('', bin_str, addr_list)
        return addr_list

    def _generate_addrs(self, cur_str, bin_str, addr_list):
        if len(bin_str) == 0:
#            print(f'adding {cur_str}')
            addr_list.append(int(cur_str, 2))
            return

        ch = bin_str[0]

        if ch == 'X':
            self._generate_addrs(cur_str + '1', bin_str[1:], addr_list)
            self._generate_addrs(cur_str + '0', bin_str[1:], addr_list)
        else:
            self._generate_addrs(cur_str + ch, bin_str[1:], addr_list)
        

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file

    # Part 1
    memory = {}
    masker = Masker()
    with open(in_file, 'r') as ff:
        for line in ff:
            line = line.rstrip().split(' = ')
            match = MEM.match(line[0])
            if match:
                mem = match.group('value')
                value = masker.mask(int(line[1]))
                memory[mem] = value
            else:
                masker.set_mask(line[1])

    total = sum([v for v in memory.values()])
    print(total)

    # Part 2
    # Getting lazier by the day instead of making
    # things nice and pretty
    memory = {}
    masker = Masker()
    with open(in_file, 'r') as ff:
        for line in ff:
            line = line.rstrip().split(' = ')
            match = MEM.match(line[0])
            if match:
                mem = match.group('value')
                addrs = masker.mask_addr(int(mem))
                for addr in addrs:
                    memory[addr] = int(line[1])
            else:
                masker.set_mask(line[1])

    total = sum([v for v in memory.values()])
    print(total)
