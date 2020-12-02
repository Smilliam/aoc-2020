from collections import defaultdict

class Password():
    def __init__(self, pwd):
        # example input: '1-3 a: abcde'
        split_str = pwd.split()

        range_vals = split_str[0].split('-')
        self._min = int(range_vals[0])
        self._max = int(range_vals[1])

        rule = split_str[1].split(':')
        self._rule = rule[0]

        self._password = split_str[2]

        self._occurrences = self._get_occurrences(self._password)

    def _get_occurrences(self, password):
        occurrences = defaultdict(int)

        for c in password:
            occurrences[c] += 1

        return occurrences

    def check_password(self):
        occurs = self._occurrences[self._rule]

        if occurs >= self._min and occurs <= self._max:
            return True

        return False

    def check_positions(self):
        first = self._password[self._min - 1]
        second = self._password[self._max - 1]

        rule = self._rule

        if first == rule and second == rule:
            return False

        if first == rule:
            return True

        if second == rule:
            return True

        return False


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Determine how many passwords follow the provided rules.')

    parser.add_argument('password_file', type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    passwords = args.password_file

    num_valid_passwords = 0
    num_valid_positions = 0
    line_count = 0
    with open(passwords, 'r') as ff:
        for line in ff:

            password = Password(line)
            if password.check_password():
                num_valid_passwords += 1

            if password.check_positions():
                num_valid_positions += 1

    print('Number of valid passwords: {}'.format(num_valid_passwords))
    print('Number of valid passwords (positional rule): {}'.format(num_valid_positions))
