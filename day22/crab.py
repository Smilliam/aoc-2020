def recursive_combat(deck_one, deck_two):
    p1_seen_sets = set()
    p2_seen_sets = set()
    while len(deck_one) and len(deck_two):
        if str(deck_one) in p1_seen_sets and str(deck_two) in p2_seen_sets:
            return True
        p1_seen_sets.add(str(deck_one))
        p2_seen_sets.add(str(deck_two))
        card_one = deck_one.pop(0)
        card_two = deck_two.pop(0)

        if card_one <= len(deck_one) and card_two <= len(deck_two):
            winner = recursive_combat(deck_one[:card_one], deck_two[:card_two])
            if winner:
                deck_one.extend((card_one, card_two))
            else:
                deck_two.extend((card_two, card_one))
        elif card_one > card_two:
            deck_one.extend((card_one, card_two))
        elif card_two > card_one:
            deck_two.extend((card_two, card_one))

        

    return len(deck_one) > 0
    

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file
    player_one = []
    player_two = []
    with open(in_file, 'r') as ff:
        ff.readline()
        line = ff.readline()
        while line != '':
            player_one.append(int(line))
            line = ff.readline().rstrip()

        ff.readline()
        line = ff.readline()
        while line != '':
            player_two.append(int(line))
            line = ff.readline().rstrip()

    p1 = player_one[:]
    p2 = player_two[:]

    while len(player_one) and len(player_two):
        one = player_one.pop(0)
        two = player_two.pop(0)

        if one > two:
            player_one.extend((one, two))
        elif two > one:
            player_two.extend((two, one))
        else:
            print('tie')

    print(f'player one: {player_one}')
    print(f'player two: {player_two}')

    deck = None
    if len(player_one):
        deck = player_one
    else:
        deck = player_two

    total = 0
    for (i, card) in enumerate(deck):
        total += card * (len(deck) - i)

    print(total)

    recursive_combat(p1, p2)

    print(f'player one: {p1}')
    print(f'player two: {p2}')
    deck = None
    if len(p1):
        deck = p1
    else:
        deck = p2

    total = 0
    for (i, card) in enumerate(deck):
        total += card * (len(deck) - i)

    print(total)
