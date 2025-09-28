from flask import Flask, render_template, request
import pickle
import pandas as pd

'''
Catboost on a déjà entrainé le modèle et on a sauvegardé le modèle dans un fichier pickle
Nous on veut construire une application web qui va charger ce modèle et faire des prédictions avec flask
'''

app = Flask(__name__) # création de l'application flask
model = pickle.load(open("catboost_model-2.pkl", "rb")) # chargement du modèle



def model_pred(features):
    '''
    Fonction pour faire des prédictions avec le modèle chargé
    '''''
    test_data = pd.DataFrame([features])
    prediction = model.predict(test_data)
    return int(prediction[0])

# definir notre application avec des routes @ ça s'appelle des décorateurs
@app.route("/", methods=["GET"])
def Home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
# une seule route qui est predict
def predict():
    '''Fonction pour faire des prédictions avec le modèle chargé
    permet de demander à l'utilisateur d'entrer les valeurs des caractéristiques
    et afficher le résultat de la prédiction sur la page web
    '''
    if request.method == "POST":
        Age = int(request.form["Age"])
        RestingBP = int(request.form["RestingBP"])
        Cholesterol = int(request.form["Cholesterol"])
        Oldpeak = float(request.form["Oldpeak"])
        FastingBS = int(request.form["FastingBS"])
        MaxHR = int(request.form["MaxHR"])
        prediction = model.predict(
            [[Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak]]
        )

        if prediction[0] == 1:
            return render_template(
                "index.html",
                prediction_text="Kindly make an appointment with the doctor!",
            )

        else:
            return render_template(
                "index.html", prediction_text="You are well. No worries :)"
            )

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # ici on va demarrer le serveur flask
    # host  = "                                 