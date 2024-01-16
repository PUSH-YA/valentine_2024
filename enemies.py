import random as rd

class enemy:

    def __init__(self,name, x,y,speed, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.dx = speed
        self.dy = speed
        self.width = width
        self.height = height
        self.health = 10

    def update(self):
        pass # TODO

    def bounce(self, x,y):
        self.dx *= -1
        self.dy *= -1

    def damage(self,attack):
        self.health -1 



class enemy_list():
    
    temp = ["nice","something"]
    
    def __init__(self,  width, height, names = temp):
        self.names = names
        self.enemies = []
        self.spawn = []
        for i in names:
            self.enemies.append(enemy(i, rd.randint(0, width), rd.randint(0, height), 1, width, height))

    def spawn_enemy(self):
        self.spawn.append(self.enemies[rd.randint(0, len(self.enemies)-1)])
        return self.spawn
    
    def update(self):
        for e in self.spawn:
            e.update()

        