from random import randint
from Level import Level
from Player import Player
from Validator import Validator
from Database import Database
from Pencil import Pencil
from Affichage import Affichage

class Casino(object):

    def __init__(self):
        self.pencil = Pencil()
        self.level = Level(1)
        self.affichage = Affichage()
        self.player = self.get_user()
        self.nb_python = 0
        self.db = Database()

   # @classmethod
    def get_user(self):
        name_user = input(self.affichage.get_txt_python())
        name_user.strip()
        return Player(name_user, 10,1)
        
    #Fonction qui lance le jeu
    def play(self):
        self.db.player_exist(self.player.username)
        self.print_rules()
        try:
            self.ask_level()
            self.reset()
            if self.enough_credit():
                print('Règles => ', self.level.try_max, 'essais et nombre entre 1 et ', self.level.nb_max)
                print('Votre solde est de : ', self.player.credit, '€ !')
                self.ask_mise()
                self.guess_number()
                self.db.load_results_in_db(self.player)
                self.play_again()
        except InterruptedError:
            self.pencil.printFail("Oh non vous avez perdu, mon nombre était {}  ".format(self.nb_python))
            self.db.load_results_in_db(self.player)
            self.play_again()

    # Fonction qui redémarre le jeu
    def reset(self):
        self.nb_python = randint(1, self.level.nb_max)
        self.validator = Validator(self.player, self.level)
        self.player.nb_coup = 0

    # Fonction qui vérifie si le joueur a assez de gain
    def enough_credit(self):
        if not self.validator.is_credit_ok():
            print(' Au revoir ! ')
            return False
        else:
            return True

    # Fonction qui propose au joueur de choisir son niveau s'il a la possibilité
    def ask_level(self): 
        level_max = self.db.get_level(self.player)
        print("Level le plus élevé atteint est {} . ".format(level_max))
        if level_max != 1:
            try:
                choixlevel = int(input("Choisissez votre level \n"))
                assert choixlevel > 0 and choixlevel <= level_max
                self.level = Level(choixlevel)
            except ValueError:
                self.pencil.printWarning("La valeur est incorrect ")
                self.ask_level()
            except AssertionError:
                self.pencil.printWarning("Saisie erronée. Veuillez saisir un nombre entre 1 et {0} ".format(level_max))
                self.ask_level()
        else:
            print("Vous allez jouez le niveau {} .".format(level_max))

    # Fonction qui demande la mise du joueur
    def ask_mise(self, string=' Le jeu commence, entrez votre mise : '):
        try:
            cmpt_credit = int(input(string))
            assert self.player.credit >= cmpt_credit > 0
            self.player.mise = cmpt_credit
        except ValueError:
            self.ask_mise("Entrez un chiffre ! : ")
        except AssertionError:
            self.ask_mise("Entrez un chiffre entre 1 et {} : ".format(self.player.credit))

    def guess_number(self):
        try:
            nb_user = int(self.ask_number())
            if self.is_same_as_nb_python(nb_user):
                self.win()
            else:
                self.guess_number()
        except ValueError:
            pass

    def win(self):
        self.player.win = True

        if self.player.nb_coup == 1:
            self.player.du_1_coup = True

        gain = self.player.get_gain()
        self.pencil.printWin('Bingo ' + str(self.player.username) + ' vous avez gagné en ' + str(self.player.nb_coup)+
                ' coup(s) et vous avez emporté '+ str(gain) + ' € !')

        self.player.gain = gain
        self.player.credit += gain
        self.level.niveauSuperieur()
        self.player.level = self.level.current
        self.pencil.printWin('Super ! Vous passez au level {} ! '.format(self.level.current))

    #fonction qui demande au player de choisir un nombre
    def ask_number(self, string="Alors mon nombre est ? "):
        try:
            if not self.validator.enough_try_remaining(self.level): 
                self.level.niveauInferieur()
                raise InterruptedError("Plus assez d'essai ! ")
            if not self.validator.get_answer_in_time(string):
                self.ask_number()
            assert 1 <= int(self.validator.answer) <= self.level.nb_max
            self.player.nb_coup += 1
        except ValueError:
            self.ask_number("Entrez un chiffre ! : ")
        except AssertionError:
            self.ask_number("Je ne comprends pas ! Enter SVP un nombre entre 1 et {} : ".format(self.level.nb_max))

        return self.validator.answer

    # Fonction qui vérifie si le nombre du joueur est égale au nombre de python
    def is_same_as_nb_python(self, nb_user):
        if nb_user < self.nb_python:
            print('Votre nbre est trop petit !')
            return False
        elif nb_user > self.nb_python:
            print('Votre nbre est trop grand !')
            return False
        else:
            return True

    # Fonction qui demande au joueur s'il veut rejouer
    def play_again(self, string="Souhaitez-vous continuer à jouer (O/N) ? "):
        if self.validator.get_answer_in_time(string):
            again = self.validator.answer.strip().lower()
            self.db.print_stats(self.player)
            if again == 'o':
                print('Nouvelle partie')
                self.play()
            elif again == 'n':
                print("Au revoir, vous finissez la partie avec {}".format(self.player.credit))
            else:
                self.play_again("Souhaitez-vous continuer à jouer (Entrez 'O' pour Oui et 'N' pour Non) ? ")
        else:
            print("Au revoir !")

    # Fonction qui affiche les règles du jeu
    def print_rules(self, string="Voulez-vous voir les regle du jeu ? o/n "):
        ans1 = str(input(string))
        ans1 = ans1.strip().lower()
        if ans1 == 'o':
            print("Voici les règles : ")
            self.regle()
        elif ans1 == 'n' or ans1 == '':
            pass
        else:
            self.print_rules("Voulez-vous voir les regle du jeu ? Répondez par 'o' ou 'n '")
    #fonction qui affiche le regele de jeu
    def regle(self):
        self.pencil.printWin(
            "Hello  " + self.player.username + ", vous avez 10 €, Très bien ! Installez vous SVP à la table de pari.Je vous expliquerai le principe du jeu ")
        self.pencil.printWin(" Je viens de penser à un nombre entre 1 et " + str(
            self.level.nb_max) + ". Devinez lequel ? \n Att : vous avez le droit à trois essais ! \n Si vous devinez "
                                 "mon nombre dès le premier coup, vous gagnez le double de votre mise ! \n  Si vous "
                                 "le devinez au 2è coup, vous gagnez exactement votre mise ! \n Si vous le devinez au "
                                 "3è coup, vous gagnez la moitiè votre mise ! \n Si vous ne le devinez pas au 3è "
                                 "coup, vous perdez votre mise et \n vous avez le droit :  de retenter votre chance "
                                 "avec l'argent qu'il vous reste pour reconquérir le level perdu.")
