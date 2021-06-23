#coding:utf-8
import psycopg2
import psycopg2.extras
import sys

#nom du dragon à saisir sur la ligne de commande
if(len(sys.argv)==1): #cette ligne de code nous permet de récuperer le nom du dragon qui sera passé en paramètre par l'utilisateur
  exit("Usage: "+sys.argv[0]+" NomDragon") #Si l'utilisateur oublie de passer en paramètre le nom de dragon, alors un message d'erreur devra s'afficher

nom_dragon = sys.argv[1] #Cette variable stocke le nom de dragon que l'utilisateur a saisi comme paramètre lors de l'éxécution

# Try to connect to an existing database
print('Connexion à la base de données...')
USERNAME="engbamekoyap" # ID num :  21927314
try: # database: nom de la base de données, user: nom de l'utilisateur, password: mot de passe qui permet d'accéder  la BDD
  conn = psycopg2.connect(database=USERNAME, user=USERNAME,host='localhost', password='1234')
except Exception as e : #Lorsque l'accès à la BDD est réfusé pour une raison quelconque alors on devra afficher un message
  exit("Connexion impossible à la base de données: " + str(e))
      
print('Connecté à la base de données')
#préparation de l'exécution des requêtes (à ne faire qu'une fois)
#En utilisant connection.cursor (), nous pouvons créer un objet curseur qui nous permet d'exécuter la commande PostgreSQL via le code source Python.
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

command = """SELECT DISTINCT * FROM dragons inner join Amours on Dragons.Dragon=%s inner join 
Repas on amours.DragonAimant=repas.Dragon inner join Nourritures on Repas.Produit= Nourritures.Produit 
WHERE dragons.dragon=DragonAimant;""" # Requête sql reliant toutes les tables

cmd_list = 'SELECT distinct dragonaimant from amours where dragonaime=%s;'

########################################################################################################
print('On va exEcuter sur la base de donnEes les requEtes: ',command)
try:
  cur.execute(command, [nom_dragon]) # Requête sql reliant toutes les tables
except Exception as e :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + command + " : " + str(e))
    
print("Récupération du résultat de la requête\n") 
print("Nombre de lignes dans le rEsultat: ", cur.rowcount)

d = cur.fetchone() # il ne peut y avoir qu'un seul résultat puisque l'attribut dragon est la clé primaire de la relation dragons
##########################################################################################################
print('On va exEcuter sur la base de donnEes les requEtes: ',cmd_list)
try:
  cur.execute(cmd_list, [nom_dragon]) # Requête sql reliant toutes les tables
except Exception as ex :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + cmd_list + " : " + str(e))
    
print("Récupération du résultat de la requête\n") 
print("Nombre de lignes dans le rEsultat: ", cur.rowcount)

liste = cur.fetchall()  # Toute la liste

##########################################################################################################
print("\n")
#traitement des résultats
page = ''
love = ''
page += d['dragon']+"a une longueur de "+str(d['longueur'])+" et "+str(d['ecailles']) + " écailles.\n"+d['enamour']+" en amour "+d['dragonaimant']+" est en relation avec " +d['dragonaime']+ " leur relation est dite '"+d['force']+"'.\n"+d['dragon']+" mange '"+d['produit']+"' d'une quantité de "+str(d['quantite'])+".\nCe produit ("+d['produit']+") contient "+str(d['calories'])+" calories.\n"
#-------------------------------------------------------------------------------
if(d['sexe']=='M'):
  page +="C'est un mâle "
else:
  page +="C'est une femelle "
page += d['enamour']

if(d['crachefeu']=='O'):
  page+=" qui crache du feu.\n"
else:
  page+=" qui ne crache pas de feu.\n"

#-----------------------------------------------------------------------------------
for l in liste:
  love += l['dragonaimant']+"\n"
#fermeture de la connexion
cur.close()
conn.close()
print(page)
print(love)

#---------------NGBAME KOYAPOLO Emmanuel 21927314---------------------------------------


