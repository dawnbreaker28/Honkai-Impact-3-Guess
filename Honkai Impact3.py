import Heroes
import random


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


def game():
    kevin_wins = 0
    v2v_wins = 0
    kosmo_wins = 0
    griseo_wins = 0
    pardofelis_wins = 0
    aponia_wins = 0
    elysia_wins = 0
    mobius_wins = 0
    hua_wins = 0
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
        result = 0
        while result == 0:
            result = fight(elysia, hua, rounds)
            # print("rounds: ", rounds, 'elysia HP', elysia.HP)
            # print("rounds: ", rounds, 'hua HP', hua.HP)
            rounds += 1
        if result == 1:
            elysia_wins += 1
        else:
            hua_wins += 1
    print('elysia win', elysia_wins, 'times')
    print('hua win', hua_wins, 'times')


if __name__ == '__main__':
    game()
