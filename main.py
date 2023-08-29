from app import loadCsvWithPandas
from flask import Flask, render_template, request, flash
import psutil

app = Flask(__name__)
app.secret_key = '6358'

used_memory = psutil.virtual_memory().used
used_memory_mb = used_memory / 1024 / 1024
print(f"Used Memory from Main: {used_memory_mb:.2f} MB")

@app.route('/', methods=['GET', 'POST'])
def index():
    game = ""  # Default value
    state = "search"  # Default value
    recommendations = None  # Default value
    chart = ""  # Initialize chart
    scatterPlot = ""  # Initialize chart

    if request.method == 'POST':
        game = request.form.get('game')
        state = request.form.get('state')

        if 'reset' in request.form:  # Check if reset button was clicked
            state = 'search'
            game = ""
            return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                                   scatter_plot=scatterPlot, state=state)

        if game not in loadCsvWithPandas.indices:
            flash(f"Title '{game}' not found in the dataframe. Please enter a valid game title.", "error")
            return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                                   scatter_plot=scatterPlot, state=state)

        state = 'reset'
        recommendations = loadCsvWithPandas.recommender(game, loadCsvWithPandas.similarity, loadCsvWithPandas.df)
        recommendations = recommendations.head(50)
        chart = loadCsvWithPandas.createBarGraph(recommendations)
        scatterPlot = loadCsvWithPandas.createPriceSentimentScatter(recommendations)

        print(f"Used Memory: {used_memory_mb:.2f} MB")

        return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                               scatter_plot=scatterPlot, state=state)
    else:
        return render_template('index.html', game=game, recommendations=recommendations, bar_chart=chart,
                               scatter_plot=scatterPlot, state=state)


if __name__ == '__main__':
    app.run(debug=True)
