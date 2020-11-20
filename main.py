from Casino import Casino
from Database import Database
from Player import Player
from Pencil import Pencil

if __name__ == '__main__':
    jeu = Casino()
    jeu.play()

'''
    p1 = Player("sam",10,1)
    db_stats(p1)

    def db_stats(player):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT player.first_login as firstlog, player.username, AVG(game.mise) as moy_mise, AVG(game.gain) as moy_gain ,MAX(game.gain) as max_gain, max(game.mise) as max_mise,MIN(game.gain) as min_gain, MIN(game.mise) as min_mise from player,game where player.username = game.username and player.username = %s"
                cursor.execute(sql,(player.username))

                data = cursor.fetchone()
                if (data == None) :
                    print("Vide")
                else :
                    
                    print("Vos meilleures statistiques".format(data['firstlog']))
                    print("Le gain le plus élevé est {}".format(data['max_gain']))
                    print("La mise la plus élevée est {}\n".format(data['max_mise']))

                    print("Vos pires statistiques")
                    print("Le gain le moins élevé est {}".format(data['min_gain']))
                    print("La mise la moins élevée est {}\n".format(data['min_mise']))

                    print("Votre mise moyenne est de  {}".format(data['moy_mise']))
                    print("Votre gain moyen est de {}\n".format(data['moy_gain']))
                    print("------------>", data)
                
                    return data
        except Exception as e :
            print(e)
            '''