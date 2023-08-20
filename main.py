import os
from app import loadCsvWithPandas
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    game = None              # Default value
    recommendations = None   # Default value
    chart = ""               # Initialize chart
    scatterPlot = ""         # Initialize chart

    if request.method == 'POST':
        game = request.form.get('game')
        recommendations = loadCsvWithPandas.recommender(game, loadCsvWithPandas.similarity, loadCsvWithPandas.df2)
        recommendations = recommendations.head(50)

        chart = loadCsvWithPandas.createBarGraph(recommendations)
        scatterPlot = loadCsvWithPandas.createPriceSentimentScatter(recommendations)

    return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                           scatter_plot=scatterPlot)


if __name__ == '__main__':
    app.run(debug=True)
