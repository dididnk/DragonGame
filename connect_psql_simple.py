#coding:utf-8
import psycopg2
import psycopg2.extras
import sys

# Try to connect to an existing database
print('Connexion à la base de données...')
USERNAME="engbamekoyap" # ID num :  21927314
try:
  conn = psycopg2.connect(host='localhost', dbname=USERNAME,user=USERNAME, password='1234')
except Exception as e :
  exit("Connexion impossible à la base de données: " + str(e))
      
print('Connecté à la base de données')
#préparation de l'exécution des requêtes (à ne faire qu'une fois)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

command = 'select * from dragons'
print('On va exécuter sur la base de données la requête: ',command)
try:
  # Lancement de la requête  
  cur.execute(command)
except Exception as e :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + command + " : " + str(e))
    
print("Récupération du résultat de la requête\n")

print("Nombre de lignes dans le résultat: ", cur.rowcount)

rows = cur.fetchall() #rows => liste de dictionnaires (chaque ligne du résultat de la requête est un dictionnaire dont la clé est le nom de l'attribut)
    
#traitement des résultats
page = ''
for d in rows:
  page += d['dragon']+" a une longueur de "+str(d['longueur'])+" et "+str(d['ecailles']) + " écailles.\n"
  if(d['sexe']=='M'):
      page +="C'est un mâle "
  else:
      page +="C'est une femelle "
  page += d['enamour']

  if(d['crachefeu']=='O'):
      page+=" qui crache du feu.\n\n"
  else:
      page+=" qui ne crache pas de feu.\n\n"

#fermeture de la connexion
cur.close()
conn.close()
print(page)


