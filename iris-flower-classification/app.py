# Import necessary libraries
from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load the data
columns = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width', 'Class_labels']
df = pd.read_csv('iris.data', names=columns)

# Load the trained SVM model
with open('SVM.pickle', 'rb') as f:
    model = pickle.load(f)


# Define route for the home page
@app.route('/')
def index():
    return render_template('index.html')


# Define route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        # Make prediction using the loaded model
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        prediction = model.predict(input_data)

        # Return the prediction result to the user
        return render_template('index.html', prediction_text='Predicted Species: {}'.format(prediction[0]))


# Define route for displaying visualizations
@app.route('/visualization')
def visualization():
    # Visualize the whole dataset
    sns.pairplot(df, hue='Class_labels')
    plt.xlabel("Features")
    plt.ylabel("Value in cm.")
    plt.title("Pairplot of Iris Dataset")
    plt.tight_layout()

    # Check if the static directory exists
    static_dir = 'static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the visualization as an image
    visualization_path = 'static/visualization.png'
    plt.savefig(visualization_path)
    plt.close()

    return render_template('visualization.html', visualization_path=visualization_path)


if __name__ == '__main__':
    app.run(debug=True)
