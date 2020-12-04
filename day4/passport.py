import re

EXPECTED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
hgt_re = re.compile('^([0-9]{3}cm|[0-9]{2}in)$')
hcl_re = re.compile('^#([0-9a-f]){6}$')
pid_re = re.compile('^[0-9]{9}$')
class Passport:
    def __init__(self, id_str):
        self._fields = {}

        key_val_list = id_str.split()
        for kv_str in key_val_list:
            kv = kv_str.split(':')
            self._fields[kv[0]] = kv[1]

    def _check_byr(self):
        byr = self._fields.get('byr')
        if not byr or len(byr) != 4:
            return False

        byr = int(byr)
        return 1920 <= byr <= 2002

    def _check_iyr(self):
        iyr = self._fields.get('iyr')
        if not iyr or len(iyr) != 4:
            return False

        iyr = int(iyr)
        return 2010 <= iyr <= 2020

    def _check_eyr(self):
        eyr = self._fields.get('eyr')
        if not eyr or len(eyr) != 4:
            return False

        eyr = int(eyr)
        return 2020 <= eyr <= 2030

    def _check_hgt(self):
        hgt = self._fields.get('hgt')
        if not hgt or not hgt_re.match(hgt):
            return False

        if 'cm' in hgt:
            hgt = int(hgt.split('cm')[0])
            return 150 <= hgt <= 193

        if 'in' in hgt:
            hgt = int(hgt.split('in')[0])
            return 59 <= hgt <= 76

    def _check_hcl(self):
        hcl = self._fields.get('hcl')
        if hcl and hcl_re.match(hcl):
            print('hcl passed: ', hcl)
            return True

        return False

    def _check_ecl(self):
        ecl = self._fields.get('ecl')
        return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def _check_pid(self):
        pid = self._fields.get('pid')
        if pid and pid_re.match(pid):
            print('pid passed: ', pid)
            return True

        return False

    def check_valid(self):
        for key in EXPECTED_FIELDS:
            if key not in self._fields:
                return False

        return True

    # this kind of poop, but this whole day kind of poop
    def check_strict_valid(self):
        return (self._check_byr() and
               self._check_iyr() and
               self._check_eyr() and
               self._check_hgt() and
               self._check_hcl() and
               self._check_hcl() and
               self._check_ecl() and
               self._check_pid())

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Determine how many passwords follow the provided rules.')

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    passports = []
    num_valid = 0
    num_strict_valid = 0
    num_lines = 0
    with open(args.in_file, 'r') as ff:
        id_str = ''

        for line in ff:
            num_lines += 1
            line = line.rstrip()
            if line == '':
                passport = Passport(id_str)
                passports.append(passport)
                id_str = ''
                if passport.check_valid():
                    num_valid += 1
                if passport.check_strict_valid():
                    num_strict_valid += 1
            else:
                id_str += ' ' + line

        if id_str != '':
            passport = Passport(id_str)
            passports.append(passport)
            if passport.check_valid():
                num_valid += 1
            if passport.check_strict_valid():
                num_strict_valid += 1


    print("num passports: " +  str(len(passports)))
    print("num lines: " + str(num_lines))
    print("num valid passports: " + str(num_valid))
    print("num strict valid passports: " + str(num_strict_valid))
