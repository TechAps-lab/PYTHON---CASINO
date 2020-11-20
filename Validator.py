from time import time

class Validator(object):

    def __init__(self, player, level):
        self.player = player
        #self.level = level
        self.answer = ''
    # Verification de credit
    def is_credit_ok(self):
        try:
            assert self.player.credit > 0
            return True
        except AssertionError:
            print("Vous n'avez plus d'argent !")
            return False
    # Fonction time pour calculer le temps de saisie par player
    def get_answer_in_time(self, string):
        try:
            start = time()
            self.answer = input(string)
            end = time()
            assert end - start < 10
            return True
        except AssertionError:
            self.player.nb_coup += 1
            print("Delais d'attente dépassé")
            return False
    # verifie combien des essais il lui reste
    def enough_try_remaining(self, level):
        try:
            assert self.player.nb_coup < level.try_max
            return True
        except AssertionError:
            self.player.credit -= self.player.mise
            print("Vous avez epuisé votre nombre d'essais.!")
            return False
