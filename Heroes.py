import random


class People:
    attack = 0
    defence = 0
    HP_max = 100
    HP = 100
    speed = 0
    stunned = False  # 混乱by v2v
    broken = 0
    sealed = False  # 封印by aponia or mobius
    silenced = False  # 沉默by aponia
    weak = False  # -6 attack by Elysia

    def __init__(self):
        pass

    def round(self, rounds, people):  # return -1 for self lost, 1 for opponent lost, 0 for peace
        self.checkBroken()
        if not self.isAlive():
            return -1
        if self.sealed:
            self.recover()
            return 0
        if self.silenced:
            self.recover_silence()
            people.HP -= self.attack - people.defence
            if not people.isAlive():
                return 1
            return 0
        else:
            if self.weak:
                self.attack -= 6
            result = self.action(rounds, people)
            if self.weak:
                self.attack += 6
                self.weak = False
            return result

    def action(self, rounds, people):
        pass  # return -1 for self lost, 1 for opponent lost

    def normal_attack(self, rounds, target):
        if not self.stunned:
            target.beingAttacked(self.attack, self)
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()

    def skill1(self, rounds, people):
        pass

    def skill2(self, rounds, people):
        pass

    def beingAttacked(self, damage, source, isPhysic=True):
        if isPhysic:
            if damage > self.defence:
                self.HP -= damage - self.defence
        else:
            self.HP -= damage

    def isStunned(self):
        return self.stunned

    def recover(self):
        self.recover_seal()
        self.recover_silence()

    def stun(self):
        self.stunned = True

    def recover_stun(self):
        self.stunned = False

    def seal(self):
        self.sealed = True

    def recover_seal(self):
        self.sealed = False

    def silence(self):
        self.silenced = True

    def recover_silence(self):
        self.silenced = False

    def checkBroken(self):
        if self.broken > 0:
            self.HP -= 4
            self.broken -= 1

    def isAlive(self):
        if self.HP > 0:
            return True
        else:
            return False


class Kevin(People):
    attack = 20
    defence = 11
    HP = 100
    speed = 21
    stunned = False

    def action(self, rounds, people):
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            return self.normal_attack(rounds, people)
        else:
            people.beingAttacked(d1 + people.defence, self)
            d2 = self.skill2(rounds, people)
            if d2 == 100:
                return 1
            if not people.isAlive():
                return 1
            return 0

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            d2 = self.skill2(rounds, people)
            if d2 == 100:
                return 1
            if not people.isAlive():
                return 1
            return 0
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if not self.isAlive():
                return -1
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
        self.skill2(rounds, people)
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            people.beingAttacked(self.attack, self)
        else:
            people.beingAttacked(int(d1), self)
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
        d1 = self.skill1(rounds, people)
        if d1 == 0:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        return 0

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.15:
                people.broken = 3
            if not people.isAlive():
                return 1
            return 0
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if random.random() < 0.15:
                self.broken = 3
            if not self.isAlive():
                return -1
            return 0

    def skill1(self, rounds, people):
        if rounds % 2 == 0:
            attack = 0
            for i in range(4):
                attack += int(random.random() * 11 + 11)
                if people.broken > 0:
                    attack += 3
                else:
                    if random.random() < 0.15:
                        people.broken = 3
                if attack - people.defence > 0:
                    people.beingAttacked(attack, self)
                attack = 0
            return 1
        return 0


class Griseo(People):
    attack = 16
    defence = 11
    HP = 100
    speed = 18
    stunned = False
    max_defence = 21
    shield = 0

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if random.random() < 0.4 and self.defence < self.max_defence:
            self.defence += 2
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        if self.shield > 0:
            self.shield = 15
            people.beingAttacked(int(self.defence), self)
        else:
            self.shield = 15

    def beingAttacked(self, damage, people, isPhysic=True):
        real_damage = damage - self.defence
        if real_damage > 0:
            if self.shield == 0:
                self.HP -= real_damage
            else:
                if real_damage >= self.shield:
                    self.HP -= real_damage - self.shield
                    self.shield = 0
                    people.beingAttacked(int(self.defence * (2 * random.random() + 2)), self)

                else:
                    self.shield -= real_damage


class Pardofelis(People):
    attack = 17
    defence = 10
    HP = 100
    speed = 24

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if random.random() < 0.3:
            people.beingAttacked(30, self)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        people.beingAttacked(30, self)
        self.HP += (30 - people.defence)
        if self.HP > 100:
            self.HP = 100


class Aponia(People):
    attack = 21
    defence = 10
    HP = 100
    speed = 30

    def action(self, rounds, people):
        if rounds % 4 == 0:
            self.skill1(rounds, people)
            if random.random() < 0.3:
                people.silence()
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        people.beingAttacked(35, self)
        people.seal()

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.3:
                people.silence()
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if random.random() < 0.3:
                self.silence()


class Elysia(People):
    attack = 21
    defence = 8
    HP = 100
    speed = 20

    def action(self, rounds, people):
        if rounds % 2 == 0:
            self.skill1(rounds, people)
            if random.random() < 0.35:
                people.beingAttacked(11 + people.defence, self)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        people.beingAttacked(int(25 * (random.random() + 1)), self)
        people.weak = True

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.35:
                people.beingAttacked(11, self, isPhysic=False)
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if random.random() < 0.35:
                self.HP -= 11


class Mobius(People):
    attack = 21
    defence = 11
    HP = 100
    speed = 23

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        people.beingAttacked(33, self)
        if random.random() < 0.33:
            people.seal()

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.33:
                people.defence = people.defence - 3
                if people.defence < 0:
                    people.defence = 0
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if random.random() < 0.33:
                self.defence = self.defence - 3
                if self.defence < 0:
                    self.defence = 0


class Hua(People):
    attack = 21
    defence = 12
    HP = 100
    speed = 15
    accumulate = False

    def action(self, rounds, people):
        if self.accumulate:
            self.defence -= 3
        if rounds % 2 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        self.defence += 3
        self.accumulate = True

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if self.accumulate:
                people.beingAttacked(int(23*random.random()+10), self, False)
                self.accumulate = False
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if self.accumulate:
                people.beingAttacked(int(23 * random.random()+10), self, False)
                self.accumulate = False

    def beingAttacked(self, damage, people, isPhysic=True):
        if isPhysic:
            if damage > self.defence:
                self.HP -= round(0.8*(damage - self.defence))
        else:
            self.HP -= round(0.8*damage)


class Eden(People):
    attack = 16
    defence = 12
    HP = 100
    speed = 16
    speed_up = False

    def action(self, rounds, people):
        if self.speed_up:
            self.speed_up = False
            self.speed = 16
        if rounds % 2 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        self.attack += 4
        self.normal_attack(rounds, people)
        self.speed = 100
        self.speed_up = True

    def normal_attack(self, rounds, people):
        if not self.stunned:
            people.beingAttacked(self.attack, self)
            if random.random() < 0.5:
                people.beingAttacked(self.attack, self)
        else:
            self.HP -= self.attack - self.defence
            self.recover_stun()
            if random.random() < 0.5:
                self.HP -= self.attack - self.defence


class Jiege(People):
    attack = 23
    defence = 9
    HP = 100
    speed = 26
    rest = False
    attack_fromHP = 0

    def round(self, rounds, people):  # return -1 for self lost, 1 for opponent lost, 0 for peace
        self.checkBroken()
        if not self.isAlive():
            return -1
        if self.rest:
            self.rest = False
            self.recover()
            return 0
        if self.sealed:
            self.recover()
            return 0
        if self.silenced:
            self.recover_silence()
            people.HP -= self.attack - people.defence
            if not people.isAlive():
                return 1
            return 0
        else:
            if self.weak:
                self.attack -= 6
            result = self.action(rounds, people)
            if self.weak:
                self.attack += 6
                self.weak = False
            return result

    def action(self, rounds, people):
        if rounds % 3 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        if self.HP > 11:
            self.HP -= 10
            people.beingAttacked(46+int(19*random.random()), self)
            self.rest = True
        else:
            self.normal_attack(rounds, self)

    def normal_attack(self, rounds, people):
        real_attack = self.attack + int((100-self.HP)/5)
        if not self.stunned:
            people.beingAttacked(real_attack, self)
        else:
            self.HP -= real_attack - self.defence
            self.recover_stun()


class Ying(People):
    attack = 24
    defence = 10
    HP = 100
    speed = 27
    miss = False

    def round(self, rounds, people):  # return -1 for self lost, 1 for opponent lost, 0 for peace
        self.miss = False
        self.checkBroken()
        if not self.isAlive():
            return -1
        if self.sealed:
            self.recover()
            return 0
        if self.silenced:
            self.recover_silence()
            people.beingAttacked(self.attack, self)
            if not people.isAlive():
                return 1
            return 0
        else:
            if self.weak:
                self.attack -= 6
            result = self.action(rounds, people)
            if self.weak:
                self.attack += 6
                self.weak = False
            return result

    def action(self, rounds, people):
        if rounds % 2 == 0:
            self.skill1(rounds, people)
        else:
            self.normal_attack(rounds, people)
        if not people.isAlive():
            return 1
        if not self.isAlive():
            return -1
        return 0

    def skill1(self, rounds, people):
        self.HP += int(4*random.random()) + 1
        if self.HP > 100:
            self.HP = 100
        people.beingAttacked(int(self.attack*1.3), self)

    def beingAttacked(self, damage, source, isPhysic=True):
        if random.random() < 0.15:
            self.miss = True
        else:
            if not self.miss:
                if isPhysic:
                    if damage > self.defence:
                        self.HP -= damage - self.defence
                else:
                    self.HP -= damage

