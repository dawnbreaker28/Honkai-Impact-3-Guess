import Heroes
import random


class Player:
    name = ''
    wins = 0

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def win(self):
        self.wins += 1


def fight(left, right, rounds):
    if left.speed < right.speed:
        r2 = right.round(rounds, left)
        if r2 == 0:
            r1 = left.round(rounds, right)
            if r1 == 0:
                return 0
            elif r1 == -1:
                return 2
            else:
                return 1
        elif r2 == -1:
            return 1
        else:
            return 2
    else:
        r1 = left.round(rounds, right)
        if r1 == 0:
            r2 = right.round(rounds, left)
            if r2 == 0:
                return 0
            elif r2 == -1:
                return 1
            else:
                return 2
        elif r1 == -1:
            return 2
        else:
            return 1


def game(a, b):
    dictionary = {
        1: 'kevin',
        2: 'elysia',
        3: 'aponia',
        4: 'eden',
        5: 'v2v',
        6: 'jiege',
        7: 'su',
        8: 'sakura',
        9: 'kosmo',
        10: 'mobius',
        11: 'griseo',
        12: 'hua',
        13: 'pardofelis'
    }
    left = Player(dictionary[a])
    right = Player(dictionary[b])
    for i in range(10000):
        rounds = 1
        kevin = Heroes.Kevin()
        v2v = Heroes.V2v()
        kosmo = Heroes.Kosmo()
        griseo = Heroes.Griseo()
        pardofelis = Heroes.Pardofelis()
        aponia = Heroes.Aponia()
        elysia = Heroes.Elysia()
        mobius = Heroes.Mobius()
        hua = Heroes.Hua()
        eden = Heroes.Eden()
        jiege = Heroes.Jiege()
        ying = Heroes.Ying()
        players = [0,
                   kevin,
                   elysia,
                   aponia,
                   eden,
                   v2v,
                   jiege,
                   7,
                   ying,
                   kosmo,
                   mobius,
                   griseo,
                   hua,
                   pardofelis
                   ]
        result = 0
        while result == 0:
            result = fight(players[a], players[b], rounds)
            # print("rounds: ", rounds, 'eden HP', players[4].HP)
            # print("rounds: ", rounds, 'jiege HP', players[6].HP)
            rounds += 1
        if result == 1:
            left.win()
        else:
            right.win()
    print(left, 'win', left.wins, 'times')
    print(right, 'win', right.wins, 'times')


if __name__ == '__main__':
    game(1, 5)
    # dictionary = {
    #     1: 'kevin',
    #     2: 'elysia',
    #     3: 'aponia',
    #     4: 'eden',
    #     5: 'v2v',
    #     6: 'jiege',
    #     7: 'su',
    #     8: 'sakura',
    #     9: 'kosmo',
    #     10: 'mobius',
    #     11: 'griseo',
    #     12: 'hua',
    #     13: 'pardofelis'
    # }
