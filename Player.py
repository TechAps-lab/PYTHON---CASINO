class Player(object):

    def __init__(self, username, credit, level):
        self.credit = credit
        self.username = username
        self.nb_coup = 0
        self.mise = 0
        self.gain = 0
        #self.player.level = 0
        self.level = level# test

        self.du_1_coup = False
        self.win = False
        
    def get_gain(self):
        if self.nb_coup == 1:
            return self.mise * 2 
        elif self.nb_coup == 2:
            return self.mise
        elif self.nb_coup == 3:
            return self.mise / 2 
        elif self.nb_coup == 4:
            return self.mise / 3
        elif self.nb_coup == 5:
            return self.mise / 4
        elif self.nb_coup == 6:
            return self.mise / 5 
        elif self.nb_coup == 7:
            return 0
        else:
            raise Exception("Vous trichez !")

