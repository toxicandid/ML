from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            try:
                df = pd.read_csv(file)
                # Perform K-Means clustering
                kmeans = KMeans(n_clusters=3, random_state=42)  # You can adjust the number of clusters as needed
                features = df[['annual_income', 'spending_score']]
                scaler = StandardScaler()
                features_scaled = scaler.fit_transform(features)
                df['cluster'] = kmeans.fit_predict(features_scaled)

                summary_stats = get_summary_stats(df)
                plot_data = analyze_data(df)
                return render_template('index.html', summary_stats=summary_stats, plot_data=plot_data)
            except Exception as e:
                flash(f'An error occurred: {str(e)}')
                return redirect(request.url)

    return render_template('index.html')

def get_summary_stats(df):
    summary_stats = df.describe().to_dict()
    formatted_summary_stats = {}
    for key, value in summary_stats.items():
        formatted_summary_stats[key.capitalize()] = {
            'Count': value['count'],
            'Mean': value['mean'],
            'Std Dev': value['std'],
            'Min': value['min'],
            '25%': value['25%'],
            '50%': value['50%'],
            '75%': value['75%'],
            'Max': value['max']
        }
    return formatted_summary_stats

def analyze_data(df):
    plots = {}

    # Scatter plot: Spending Score vs Annual Income
    scatter_plot = BytesIO()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="annual_income", y="spending_score", data=df, hue='cluster', palette='viridis', s=60)
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.title('Customer Segmentation')
    plt.tight_layout()
    plt.savefig(scatter_plot, format='png')
    scatter_plot.seek(0)
    plots['scatter_plot'] = base64.b64encode(scatter_plot.getvalue()).decode('utf-8')

    # Distribution plot: Age
    age_plot = BytesIO()
    plt.figure(figsize=(8, 6))
    sns.histplot(df["age"], kde=True, color="orange")
    plt.title('Distribution of Age')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(age_plot, format='png')
    age_plot.seek(0)
    plots['age_plot'] = base64.b64encode(age_plot.getvalue()).decode('utf-8')

    # Distribution plot: Gender
    gender_plot = BytesIO()
    plt.figure(figsize=(6, 4))
    sns.countplot(x='gender', data=df, hue='cluster', palette='viridis')
    plt.title('Gender Analysis')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(gender_plot, format='png')
    gender_plot.seek(0)
    plots['gender_plot'] = base64.b64encode(gender_plot.getvalue()).decode('utf-8')

    return plots

if __name__ == "__main__":
    app.run(debug=True)
