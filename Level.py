import json


class Level:

    def __init__(self, level):
        data = self.unencode_JSON()[0]
        try:
            self.current = int(data[str(level)]["level"])
            self.try_max = data[str(level)]["try_max"]
            self.nb_max = data[str(level)]["nb_max"]
        except KeyError:
            self.current = int(data[str(3)]["level"])
            self.try_max = data[str(3)]["try_max"]
            self.nb_max = data[str(3)]["nb_max"]


    @classmethod
    def unencode_JSON(cls):
        with open('level.json') as f:
            data = [json.load(f)]
        return data

    def __str__(self):
        return "Level " + str(self.current)

    #Methode qui augmente le level
    def niveauSuperieur(self):
        if self.current < 3 :
            self.current = self.current + 1
        return self.current

    #Methode qui diminue le level
    def niveauInferieur(self):
        if self.current > 1 :
            self.current = self.current - 1
        return self.current
