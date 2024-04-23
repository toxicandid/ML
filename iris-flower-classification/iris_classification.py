import numpy as np
import pandas as pd
import pickle

def predict_species(sepal_length, sepal_width, petal_length, petal_width):
    # Load the SVM model
    with open('SVM.pickle', 'rb') as f:
        model = pickle.load(f)

    # Predict the species
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

    # Convert numerical prediction to species label
    if prediction == 0:
        return "Setosa"
    elif prediction == 1:
        return "Versicolor"
    elif prediction == 2:
        return "Virginica"
    else:
        return "Unknown"
