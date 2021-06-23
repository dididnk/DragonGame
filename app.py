from flask import *
import psycopg2
import psycopg2.extras
import sys
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)

#Variables globales
USERNAME="engbamekoyap" # ID num :  21927314

liste_dragon = []
liste_pretendant = []
liste_regime = []

# page d'accueil
@app.route("/")
def accueil():
  return render_template("form2.html") # Formulaire de base 
#Fonction permettant de gérer la connexion à la base de donées (la partie Server)
@app.route("/home")
def dragon_saisi():
  # Appel des variables globales
  global liste_dragon
  global liste_pretendant
  global liste_regime 
  try: 
    # database: nom de la base de données, user: nom de l'utilisateur, password: mot de passe qui permet d'accéder  la BDD
    #En utilisant connection.cursor (), nous pouvons créer un objet curseur qui nous permet d'exécuter la commande PostgreSQL via le code source Python.
    conn = psycopg2.connect(database=USERNAME, user=USERNAME,host='localhost', password='1234')
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      nom_dragon = request.args.get('input_dragon') # recupère le nom de dragon saisi
      test_pretendant = request.args.get('pretendant')!=None # test si le checkbox est coché ou pas
      test_regime = request.args.get('regime')!=None # test si le checkbox est coché ou pas
      #------------------------------------Requête SQL----------------------------------------------------

      command = 'SELECT dragon FROM dragons' # Requête sql pour récupérer les noms des dragons
      cur.execute(command)
      liste_dragon = cur.fetchall() #liste des noms des dragons
      
      command1 = 'SELECT produit from Repas where dragon=%s' # Requête sql pour le régimes
      cur.execute(command1,[nom_dragon]) 
      liste_regime = cur.fetchone() # Récupère le nom de régime

      command2 = 'SELECT dragonaimant from Amours where dragonaime=%s' # Requête sql pour les prétendants
      cur.execute(command2,[nom_dragon]) 
      liste_pretendant = cur.fetchall() # Liste des noms des pretendants

      #-------------------------------------Fermeture de la connection------------------------------------------
      cur.close()
      conn.close()
      #---------------------------------------Vérification des conditions---------------------------------------- 
      if(test_regime == False):
        liste_regime = "L'utilisateur n'a pas selectionné le regime alimentaire !"
      if(test_pretendant == False):
        liste_pretendant = "L'utilisateur n'a pas selectionné l'option pour les prétendants!"
      if(liste_pretendant == ""):
        liste_pretendant = "Le dragon n'a pas des prétendants!"
      for n in liste_dragon:
        if [nom_dragon] == n:
          return render_template("affichage.html",liste_pretendant = liste_pretendant, liste_regime = liste_regime) # Affiche ce qui est demandé
      return redirect(url_for('error_dragon', error="le dragon n'existe pas")) # Retourne un message d'erreur au cas contraire     
  #---------------------------------------Gestion d'erreur avec la base de données---------------------------------------- 
    except Exception as e :
      cur.close()
      conn.close()
      exit("impossible d'xecuter les commandes: ", e)
  except Exception as e : 
    cur.close()
    conn.close()
    exit("Connexion impossible à la base de données: ", e)

# Page d'accueil du jeux
@app.route("/home_jeu")
def home_jeux():
  liste_complete = []
  for i in liste_dragon: # Parcours la liste des drag
    liste_complete.append(i['dragon'])
  return render_template("amours.html", liste_DAimant = liste_complete, liste_DAime = liste_complete) # renvoie le menu du jeux en remplissant les éléments qui composent le jeux (noms des dragons)

@app.route("/accueil")
def dragon_selection():
  nom_DAime = ''
  try: 
    # database: nom de la base de données, user: nom de l'utilisateur, password: mot de passe qui permet d'accéder  la BDD
    #En utilisant connection.cursor (), nous pouvons créer un objet curseur qui nous permet d'exécuter la commande PostgreSQL via le code source Python.
    conn = psycopg2.connect(database=USERNAME, user=USERNAME,host='localhost', password='1234')
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      nom_DAimant = request.args.get('input_aimant') # recupère le nom de dragon aimant
      nom_DAime = request.args.get('input_aime') # recupère le nom de dragon aimé
      #------------------------------------Requête SQL----------------------------------------------------

      cmd_amour = 'SELECT DragonAime from Amours where DragonAimant=%s' # Requête sql pour le dragon aimant
      cur.execute(cmd_amour,[nom_DAimant]) 
      l = cur.fetchone() # Récupère le nom de régime
      #-------------------------------------Fermeture de la connection------------------------------------------
      cur.close()
      conn.close()
      #---------------------------------------Vérification des conditions---------------------------------------- 
      if nom_DAime == l['dragonaime']:
        return render_template("lesAmoureux.html",DAimant = nom_DAimant, DAime = nom_DAime) # Affiche ce qui est demandé
      return redirect(url_for('home_jeux'))
#---------------------------------------Gestion d'erreur avec la base de données---------------------------------------- 
    except Exception as e :
      cur.close()
      conn.close()
      exit("impossible d'xecuter les commandes: ", e)
  except Exception as e : 
    cur.close()
    conn.close()
    exit("Connexion impossible à la base de données: ", e)

#Cette fonction nous permet de gérer l'erreur lorsque le dragon n'y est pas dans la table Dragons
@app.route("/error_dragon")
def error_dragon():
  error = request.args.get('error')
  return render_template("form2.html",hasError=error)

#Cette fonction nous permet de gérer l'erreur lorsque le dragon aimant et dragon aimé ne sont pas amoureux
@app.route("/error_dragon_love")
def error_dragon_love():
  error = request.args.get('error')
  return render_template("amours.html",hasErrorlove=error)

#Cette fonction nous permet d'afficher la liste des dragons
@app.route('/dragonsListe')
def dragon_liste():
  dragons = ''
  for c in liste_dragon: #pour chaque entrée du tableau liste
    dragons += c['dragon']+"</br>" #la variable c est un dictionnaire pour chaque dragon. On veut les données associées à la 'dragon'
  return "<b>La liste complète des dragons :</b></br></br><p>"+dragons+"</p></br><a href='/'>retour au menu</a>"

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)

# test : http://127.0.0.1:5000/