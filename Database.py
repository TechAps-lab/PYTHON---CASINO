import pymysql
import datetime

class Database:

    def __init__(self):
        self.connection = pymysql.connect(host='mysql-rootgroup5.alwaysdata.net',
                             user='218931',
                             password='lpinfo22',
                             db='rootgroup5_1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    # enregistrer les donnees dans la base
    def load_results_in_db(self, player):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `game` (`username`, `level_max`, `gain`, `mise`, `du_1e_coup`, `nb_try`, `win`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (player.username, player.level, player.gain, player.mise, player.du_1_coup, player.nb_coup, player.win))
                self.connection.commit()

                print(player.username, player.level, player.gain, player.mise, player.du_1_coup, player.nb_coup, player.win)

        except Exception as e :
            print(e)

    def print_top(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT player.username, gain from player,game where player.username = game.username order by gain desc"
                cursor.execute(sql)
                data = cursor.fetchmany(3)
                print(data)
        except Exception as e :
            print(e)
    #fonction qui verifie si le nom player existe dans la base
    def player_exist(self,player_name):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT username from player where username = %s"
                cursor.execute(sql,(player_name))

            oneRow = cursor.fetchone()
            date = datetime.datetime.now()
            if oneRow == None :
                with self.connection.cursor() as cursor:
                    sql =  "Insert into player (username, first_login,level,credit) values (%s,%s,%s,%s) "

                    cursor.execute(sql, (player_name, date,1,10 ))
                    self.connection.commit()
        except Exception as e:
            print("ERROR DB")

    # Fonction qui affiche les statistiques
    def db_stats(self,player):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT player.first_login as firstlog, player.username, AVG(game.mise) as moy_mise, AVG(game.gain) as moy_gain ,MAX(game.gain) as max_gain, max(game.mise) as max_mise,MIN(game.gain) as min_gain, MIN(game.mise) as min_mise from player,game where player.username = game.username and player.username = %s"
                cursor.execute(sql,(player.username))

                data = cursor.fetchone()
                if (data == None) :
                    print("Vide")
                else :
                    '''
                    print("Vos meilleures statistiques")
                    print("Le gain le plus élevé est {}".format(data['max_gain']))
                    print("La mise la plus élevée est {}\n".format(data['max_mise']))

                    print("Vos pires statistiques")
                    print("Le gain le moins élevé est {}".format(data['min_gain']))
                    print("La mise la moins élevée est {}\n".format(data['min_mise']))

                    print("Votre mise moyenne est de  {}".format(data['moy_mise']))
                    print("Votre gain moyen est de {}\n".format(data['moy_gain']))
                    print("------------>", data)
                    '''
                    return data
        except Exception as e :
            print(e)

    def db_win_stats (self,player):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT Count(*) as total from player,game where player.username = game.username and player.username = %s"
                cursor.execute(sql,(player.username))

                data = cursor.fetchone()
                nb_de_partie = data["total"]

                sql = "SELECT sum(game.nb_try) as nb_try,Count(game.win) as total_win from player,game where player.username = game.username and player.username = %s and game.win = True"
                cursor.execute(sql,(player.username))
                data_win = cursor.fetchone()
                pourcentage_win = 0
                nb_try_win = 0

                if data_win["total_win"] != None or data_win["nb_try"] != None:
                    pourcentage_win = ((int( data_win["total_win"]) / int(nb_de_partie)) * 100)
                    nb_try_win = (int(data_win["nb_try"]) / int(nb_de_partie))
                    pourcentage_win = round(pourcentage_win,1)


            if (data == None or pourcentage_win == 0 or nb_try_win == 0) :
                print("Pas de statistiques générales pour vous \n")
            else :
                print("Le pourcentage de réussite est de {} %".format(pourcentage_win))
                print("Votre nombre de tentatives moyen pour réussir est de {} \n".format(nb_try_win))
        except Exception as e:
            print(e)

    # Fonction qui affiche les statistiques
    def print_stats(self,player):
         self.db_stats(player)
         self.db_win_stats(player)

    #Fonction qui récupère le level du joueur
    def get_level(self,player):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT `level_max` FROM `game` WHERE `username` = %s ORDER BY `game`.`level_max` DESC"
                cursor.execute(sql,(player.username))
            oneRow = cursor.fetchone()
            if oneRow == None :
                return 1
            else :
                integer_level = int(oneRow["level_max"])
                return integer_level
        except Exception as e:
            print(e)
