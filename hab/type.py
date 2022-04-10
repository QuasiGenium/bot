class Animal:
    def __init__(self, name, a, h, tier, model, code):
        self.code = code
        self.name = name
        self.level = 1
        self.number = 1
        self.tier = tier
        self.x = 0
        self.food = ''
        self.a_now = 0
        self.h_now = 0
        self.a = a
        self.h = h
        self.model = model
        self.info = ''

    def __str__(self):
        return self.model

    def move(self, x):
        self.x = x - 1

    def info(self):
        return self.info

    def eat(self, food):
        self.food = food

    def synergy(self):
        if self.number != 6:
            self.number += 1
            self.a += 1
            self.h += 1
            if self.number in [3, 6]:
                self.level += 1

    def code(self):
        return ';'.join(list(map(str, [self.code, self.number, self.level, self.a, self.h, self.a_now, self.h_now])))

    def faint(self):
        pass

    def sell(self):
        pass

    def level_up(self):
        pass

    def friend_summon(self):
        pass

    def start_battle(self):
        pass

    def buy(self):
        pass

    def before_attack(self):
        pass

    def hurt(self):
        pass

    def start_turn(self):
        pass

