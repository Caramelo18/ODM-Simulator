class Person:
    def __init__(self, zone):
        self.origin = zone
        self.step = 0

    def __str__(self):
        return 'Oi'

    def __repr__(self):
        return 'Person from {}'.format(self.origin)

    def evolve(self):
        self.step += 1
    
    def get_origin(self):
        return self.origin
    
    def get_step(self):
        return self.step