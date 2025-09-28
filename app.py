"""Application Flask : chargement du modèle CatBoost et prédiction."""

from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)
# ⚠️ Assure-toi que le paquet catboost est installé pour (un)pickle le modèle
#     (ajoute `catboost` dans requirements.txt si nécessaire)
model = pickle.load(open("catboost_model-2.pkl", "rb"))


def model_pred(features: dict) -> int:
    """Fait une prédiction avec le modèle chargé à partir d'un dict de features."""
    test_data = pd.DataFrame([features])
    prediction = model.predict(test_data)
    return int(prediction[0])


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Récupère les valeurs du formulaire et retourne la prédiction."""
    if request.method == "POST":
        Age = int(request.form["Age"])
        RestingBP = int(request.form["RestingBP"])
        Cholesterol = int(request.form["Cholesterol"])
        Oldpeak = float(request.form["Oldpeak"])
        FastingBS = int(request.form["FastingBS"])
        MaxHR = int(request.form["MaxHR"])

        # même ordre que pendant l'entraînement
        prediction = model.predict(
            [[Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak]]
        )

        if int(prediction[0]) == 1:
            msg = "Kindly make an appointment with the doctor!"
        else:
            msg = "You are well. No worries :)"

        return render_template("index.html", prediction_text=msg)

    return render_template("index.html")


if __name__ == "__main__":
    # en prod, on utilise un serveur (gunicorn/uvicorn). Ici c'est pour debug local.
    app.run(host="0.0.0.0", port=5000, debug=True)
