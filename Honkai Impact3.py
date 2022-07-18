import random


class People:
    attack = 0
    defence = 0
    HP_max = 100
    HP = 0
    speed = 0
    stunned = False
    broken = 0

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

    def checkBroken(self):
        if self.broken > 0:
            self.HP -= 4
            self.broken -= 1
        if self.HP < 1:
            return -1


class Kevin(People):
    attack = 20
    defence = 11
    HP = 100
    speed = 21
    stunned = False

    def action(self, rounds, people):
        d0 = self.checkBroken()
        if d0 == -1:
            return -1
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
        d0 = self.checkBroken()
        if d0 == -1:
            return -1
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
                people.beingAttacked(int(d1))
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


class Kosmo(People):
    attack = 19
    defence = 11
    HP = 100
    speed = 19
    stunned = False
    activate = False

    def action(self, rounds, people):
        d0 = self.checkBroken()
        if d0 == -1:
            return -1
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            if self.isStunned():
                self.HP -= self.attack - self.defence
                self.recover()
                if random.random() < 0.15:
                    self.broken = 3
                if self.HP < 0:
                    return -1
            else:
                people.beingAttacked(self.attack)
                if random.random() < 0.15:
                    people.broken = 3
        if people.HP < 1:
            return 1
        return 0

    def skill1(self, rounds, people):
        if rounds % 2 == 0:
            attack = 0
            for i in range(4):
                attack += int(random.random()*11 + 11)
                if people.broken > 0:
                    attack += 3
                else:
                    if random.random() < 0.15:
                        people.broken = 3
                people.beingAttacked(attack)
                attack = 0
            return 1
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
    kosmo_wins = 0
    for i in range(1000):
        rounds = 1
        kevin = Kevin()
        v2v = V2v()
        kosmo = Kosmo()
        result = 0
        while result == 0:
            result = fight(v2v, kosmo, rounds)
            rounds += 1
        if result == 1:
            v2v_wins += 1
        else:
            kosmo_wins += 1
    print('v2v win ', v2v_wins, ' times')
    print('kosmo win ', kosmo_wins, ' times')


if __name__ == '__main__':
    game()
