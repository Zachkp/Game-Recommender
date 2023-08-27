from app import loadCsvWithPandas
from flask import Flask, render_template, request, flash
import psutil

app = Flask(__name__)
app.secret_key = '6358'


@app.route('/', methods=['GET', 'POST'])
def index():
    game = None  # Default value
    recommendations = None  # Default value
    chart = ""  # Initialize chart
    scatterPlot = ""  # Initialize chart

    if request.method == 'POST':
        game = request.form.get('game')

        if game not in loadCsvWithPandas.indices:
            flash(f"Title '{game}' not found in the dataframe. Please enter a valid game title.", "error")
            return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,

                                   scatter_plot=scatterPlot)
        recommendations = loadCsvWithPandas.recommender(game, loadCsvWithPandas.similarity, loadCsvWithPandas.df2)
        recommendations = recommendations.head(50)
        chart = loadCsvWithPandas.createBarGraph(recommendations)
        scatterPlot = loadCsvWithPandas.createPriceSentimentScatter(recommendations)

        used_memory = psutil.virtual_memory().used
        used_memory_mb = used_memory / (1024 * 1024)

        print(f"Used Memory: {used_memory_mb:.2f} MB")

    return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                           scatter_plot=scatterPlot)


if __name__ == '__main__':
    app.run(debug=True)
