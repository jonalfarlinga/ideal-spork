class Action:
    def __init__(self, name, cooldown, fn):
        self.name = name
        self.cooldown = cooldown
        self.cur_cd = 0
        self.fn = fn

    def __str__(self):
        return "Action: " + self.name

    def __repr__(self):
        return self.__str__()

    def tick(self):
        if self.cur_cd > 0:
            self.cur_cd -= 1
