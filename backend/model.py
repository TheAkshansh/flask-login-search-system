from flask import Flask, request, session, render_template
from sklearn import tree
import pandas as pd

from backend import app

classifier = tree.DecisionTreeClassifier()
data = {
    'Ear Size ': [2.4, 0.13, 4.0, 0.05, 1.2, 0.17],
    'Body Size ': [27.0, 2.0, 4.2, 10.3, 20.1, 5.1],
    'Eyes Size ': [0.17, 0.02, 0.03, 0.15, 0.8, 0.12],
    'Heart Length ': [1.5, 0.12, 0.2, 2.1, 1.2, 2.4],
    'Endangered Animals': ['Blue Whale', 'White Tailed Deer', 'Black Rhinos', 'Hawksbill turtle',
                           'Sumatran elephant', 'Sunda tiger']
}

df = pd.DataFrame(data)

data_features = df[['Ear Size ', 'Body Size ', 'Eyes Size ', 'Heart Length ']]
target = df['Endangered Animals']

classifier.fit(data_features, target)


def predict_species(new_features):
    prediction = classifier.predict([new_features])
    return prediction[0]


example_features = [2.4, 27.0, 0.17, 1.5]
print('The predicted Endangered Animals is: ', predict_species(example_features))


@app.route("/model")
def model():
    if 'email' in session:
        return render_template("model.html")
    else:
        userAddedStatus="User not logged in yet, please login then try again.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)


vari = ("The killing of this animal for its pelts, bones, teeth, and claws which are subsequently sold on the "
        "black market has a detrimental effect on the species and is one the cause of its extinction.")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'email' in session:
        feature1 = request.form.get("feature1")
        feature2 = request.form.get("feature2")
        feature3 = request.form.get("feature3")
        feature4 = request.form.get("feature4")

        print("feature1: ", feature1)
        userfeatures = [feature1, feature2, feature3, feature4]
        print("userfeatures:", userfeatures)

        prediction = classifier.predict([userfeatures])
        modelprediction = prediction[0], (vari)
        return render_template("model.html", predictedAnimal=modelprediction)
    else:
        userAddedStatus="User not logged in yet, please login then try again.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)

