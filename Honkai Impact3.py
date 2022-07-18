import random


class People:
    attack = 0
    defence = 0
    HP_max = 100
    HP = 0
    speed = 0
    stunned = False

    def __init__(self):
        pass

    def action(self, rounds, people):
        pass  # return -1 for self lost, 1 for opponent lost

    def skill1(self, rounds, people):
        pass

    def skill2(self, rounds, people):
        pass

    def beingAttacked(self, damage):
        self.HP -= damage - self.defence

    def isStunned(self):
        return self.stunned

    def stun(self):
        self.stunned = True

    def recover(self):
        self.stunned = False


class Kevin(People):
    attack = 20
    defence = 11
    HP = 100
    speed = 21
    stunned = False

    def action(self, rounds, people):
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            if self.isStunned():
                self.HP -= self.attack - self.defence
                self.recover()
                if self.HP < 0:
                    return -1
            else:
                people.beingAttacked(self.attack)
                d2 = self.skill2(rounds, people)
                if d2 == 100:
                    return 1
        else:
            people.beingAttacked(d1 + people.defence)
            d2 = self.skill2(rounds, people)
            if d2 == 100:
                return 1
        if people.HP < 1:
            return 1
        return 0

    def skill1(self, rounds, people):
        if rounds % 3 == 0:
            self.attack += 5
            return 25
        else:
            return 0

    def skill2(self, rounds, people):
        if not self.stunned:
            print(people.HP)
            print(people.HP_max)
            if people.HP < people.HP_max * 0.3:
                if random.random() < 0.3:
                    return 100
        return 0


class V2v(People):
    attack = 20
    defence = 12
    HP = 100
    speed = 25
    stunned = False
    activate = False

    def action(self, rounds, people):
        if self.isStunned():
            self.HP -= self.attack - self.defence
            self.recover()
            if self.HP < 0:
                return -1
        else:
            self.skill2(rounds, people)
            d1 = self.skill1(rounds, people)
            if d1 == 0:
                people.beingAttacked(self.attack)
            else:
                people.beingAttacked(int(d1) + people.defence)
            if people.HP < 0:
                return 1
        return 0

    def skill1(self, rounds, people):
        if rounds % 3 == 0:
            people.stun()
            return self.attack
        return 0

    def skill2(self, rounds, people):
        if self.HP < 31 and not self.activate:
            self.HP += int(random.random() * 10 + 10)
            people.HP += int(random.random() * 10 + 10)
            self.attack += int(13 * random.random() + 2)
            self.activate = True
        return 0


def fight(left, right, rounds):
    if left.speed < right.speed:
        r2 = right.action(rounds, left)
        if r2 == 0:
            r1 = left.action(rounds, right)
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
        r1 = left.action(rounds, right)
        if r1 == 0:
            r2 = right.action(rounds, left)
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
    v2v_wins = 0
    kevin_wins = 0
    for i in range(1000):
        rounds = 1
        kevin = Kevin()
        v2v = V2v()
        result = fight(kevin, v2v, rounds)
        while result == 0:
            rounds += 1
            result = fight(kevin, v2v, rounds)
            print('rounds', rounds, 'kevin HP:', kevin.HP)
            print('rounds', rounds, 'v2v HP:', v2v.HP)
        if result == 1:
            kevin_wins += 1
        else:
            v2v_wins += 1
    print('v2v win ', v2v_wins, ' times')
    print('kevin win ', kevin_wins, ' times')


if __name__ == '__main__':
    game()
