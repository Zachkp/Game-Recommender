import os
from app import loadCsvWithPandas
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    game = None  # Default value
    recommendations = None  # Default value

    if request.method == 'POST':
        game = request.form.get('game')
        recommendations = loadCsvWithPandas.recommender(game, loadCsvWithPandas.similarity, loadCsvWithPandas.df2)
        recommendations = recommendations.head(25)

    return render_template('index.html', game=game, recommendations=recommendations)


#@app.route('/', methods=['GET', 'POST'])
#def table():
#    if request.method == 'POST':
#        game = request.form.get('game')
#        recommendations = loadCsvWithPandas.recommender(game, loadCsvWithPandas.similarity, loadCsvWithPandas.df2)
#        return render_template('index.html', data=recommendations.head(10))

def main():
    recommendations = loadCsvWithPandas.recommender("Factorio", loadCsvWithPandas.similarity, loadCsvWithPandas.df2)
    # print(recommendations.head(10))
    # loadCsvWithPandas.createGraph(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
