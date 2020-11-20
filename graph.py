from Affichage import Affichage
from pygame.locals import *
import time
import pygame

class Graph(object):
    def __init__(self):
        self.affichage = Affichage()


    def interface_graph(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        picture = pygame.image.load('assets/bg.jpg') # Importe l'image de fond
        window = (1080, 720)
        pygame.init()
        screen = pygame.display.set_mode(window)

        # Gestion de la police d'ecriture
        font = pygame.font.SysFont(None, 20)

        # Variables qui affiche le texte du jeu
        jeu_aff = "Le jeu est ici ..."
        img_jeu_aff = font.render(jeu_aff, True, WHITE)
        # Box qui affiche le jeu
        rect_jeu = img_jeu_aff.get_rect()
        rect_jeu.topleft = (370, 50)

        # Variable case affichage 'Entrez un nombre ici : '
        entre_nb = "Espace de saisie : "
        img_entrer_nb = font.render(entre_nb, True, WHITE)
        # Box qui affiche --> 'Entrez un nombre ici : '
        rect_aff = img_entrer_nb.get_rect()
        rect_aff.topleft = (370, 350)

        # Variables case ou le joueur peut entrer un nombre
        txt = ""
        img = font.render(txt, True, RED)
        # Box qui permet d'entrer un nombre, et le curseur
        rect = img.get_rect()
        rect.topleft = (520, 350)
        cursor = Rect(rect.topright, (3, rect.height))

        running = True
        background = picture

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if len(txt)>0:
                            txt = txt[:-1]
                    else:
                        txt += event.unicode
                    img = font.render(txt, True, RED)
                    rect.size=img.get_size()
                    cursor.topleft = rect.topright
                    rect_aff.size=img_entrer_nb.get_size()

            screen.blit(background, (50, 0)) # Affiche le background dans la fenetre
            screen.blit(img_jeu_aff, rect_jeu) # Affiche le jeu dans la fenetre
            screen.blit(img, rect) # Affiche le curseur et le input dans la fenetre
            screen.blit(img_entrer_nb, rect_aff) # Affiche le 'Entrez un nombre ici : ' dans la fenetre
            if time.time() % 1 > 0.5:
                pygame.draw.rect(screen, RED, cursor)
            pygame.display.update()

        pygame.quit()