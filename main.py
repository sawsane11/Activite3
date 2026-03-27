# Importation de Flask
# render_template
# et le module random pour l'aléatoire
from flask import Flask, render_template, request, session, redirect
from questions import questions
from resultat import resultats, noms

from os import urandom
# On crée l'application = instance de la classe Flask
app = Flask(__name__)

app.secret_key = urandom(32)
# On crée le route pour la page d'accueil avec le décorateur @app
#  @app.route() associe une adresse URL à une fonction
# "/" pour la page d'accueil
@app.route("/")
def index():

    session["numero_question"] = 0

    session["score"] = {"E":0 , "A":0, "L":0, "J":0}

    return render_template("index.html")

@app.route("/question")
def question():

    global questions

    numero = session["numero_question"]
    print(numero)
    print(len(questions))
    if numero < len(questions):
    
        enonce_question = questions[numero]["enonce"]

        symboles_et_reponses = questions[numero].copy()



        symboles_et_reponses.pop("enonce")

        reponses = list(symboles_et_reponses.values())

        symboles = list(symboles_et_reponses.keys())

        session["symboles"] = symboles

        return render_template("question.html", enonce_question=enonce_question, reponses=reponses, symboles=symboles)

    else:
        # On recupère le score et notamment le symbole qui a eu le plus de réponse associé
        # Sorted trie les scores et renvoie une liste
        # reverse = True -> la liste est triée par ordre décroissant 
        scores_tries = sorted(session["score"], key = session["score"].get, reverse = True)
        # On récupère le symbole qui a le plus de points -> INITIAL DU GAGNANT
        gagnant = scores_tries[0]
        # On recup le nom du gagnant
        nom_gagnant = noms[gagnant]
        # On récupère la description correspondante
        resultat_description = resultats[gagnant]
        return render_template("resultats.html", nom_gagnant = nom_gagnant ,resultat_description = resultat_description)
    
@app.route("/reponse/<numero>")
def reponse(numero):
    # On récupère le symbole associé à la réponse sélectionné
    # conversion de numero : str -> int car on l'utilise comme indice pour récupérer le bon symbole
    symbole = session["symboles"][int(numero)]
    # On incrémente le score correspondant
    session["score"][symbole] += 1
    # On incrémente le cookie numero_question pour passer à la suivante
    session["numero_question"] +=1 
    # On redirige vers  la question suivante
    return redirect("/question")
####################################
#  TOUJOURS A LA FIN DU CODE       #
####################################
# Lancement de l'application
# HOST : précise qui a accès au serveur Flask (0.0.0.0 = toutes les adresses de la machines )
# Port d'entrée au serveur via le port 81
app.run(host="0.0.0.0", port = 81) 