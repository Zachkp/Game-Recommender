import pandas as pd
import numpy as np
import os
import io
import base64

import psutil
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../files/steam_games.csv"),
                 usecols=["name", "desc_snippet", "popular_tags", "genre", "original_price", "all_reviews"],
                 na_filter=True)
df = pd.DataFrame(df.dropna())

# Memory Usage Testing
df.info(verbose=False, memory_usage="deep")
used_memory = psutil.virtual_memory().used
used_memory_mb = used_memory / 1024 / 1024
print(f"Used Memory from loadCsvWithPandas: {used_memory_mb:.2f} MB")

tfidf = TfidfVectorizer(stop_words="english")
matrix = tfidf.fit_transform(df["desc_snippet"])

tfidf.get_feature_names_out()
matrix.toarray()

similarity = cosine_similarity(matrix)

indices = pd.Series(df.index, index=df['name'])
indices = indices[~indices.index.duplicated(keep='last')]
asd

def recommender(title, cos_similarity, dataframe):
    game_index = indices[title]
    similarity_scores = pd.DataFrame(cos_similarity[game_index], columns=["score"])
    game_indices = similarity_scores.sort_values("score", ascending=False).index

    recommended_games = dataframe.iloc[game_indices]

    # Extract sentiment, percentage, and total reviews from all_reviews column
    recommended_games['review_sentiment'] = recommended_games['all_reviews'].str.extract(r'([A-Za-z\s]+),')[0]
    recommended_games['review_percentage'] = recommended_games['all_reviews'].str.extract(r'(\d+)%')[0]
    recommended_games['review_percentage'] = recommended_games['review_percentage'].fillna(-1).astype(int)
    recommended_games['total_reviews'] = recommended_games['all_reviews'].str.extract(r'of the (\d+)')[0]
    recommended_games['total_reviews'] = recommended_games['total_reviews'].str.replace(',', '').fillna(-1).astype(int)

    # Filter by games with Very Positive, Mostly Positive, or Overwhelmingly Positive reviews (>= 75%)
    positive_reviews = ['Positive', 'Very Positive', 'Mostly Positive', 'Overwhelmingly Positive']
    recommended_games = recommended_games[
        (recommended_games['review_sentiment'].isin(positive_reviews)) &
        (recommended_games['total_reviews'] >= 50)
        ]

    um = psutil.virtual_memory().used
    umMB = um / 1024 / 1024
    print(f"Used Memory from recommender: {umMB:.2f} MB")

    return recommended_games[['name', 'genre', 'original_price', 'review_sentiment']]


def createBarGraph(recommendations):
    # Convert original_price column to numeric and handle non-numeric values
    recommendations['original_price'] = recommendations['original_price'].str.replace('[\$,]', '', regex=True)
    recommendations['original_price'] = pd.to_numeric(recommendations['original_price'], errors='coerce')

    # Handle 'Free To Play' values
    recommendations.loc[recommendations['original_price'].isnull(), 'original_price'] = 0

    # Drop rows with missing or non-numeric prices
    recommendations = recommendations.dropna(subset=['original_price'])

    # Ensure the original_price column contains only finite numeric values
    recommendations = recommendations[recommendations['original_price'].notnull() &
                                      np.isfinite(recommendations['original_price'])]

    # Define price brackets for the bar graph
    price_bins = [0, 10, 20, 30, 40, 50, float('inf')]  # Define your desired price brackets
    labels = ['$0-$10', '$11-$20', '$21-$30', '$31-$40', '$41-$50', '$50+']

    # Categorize prices into the specified brackets
    price_counts, _ = np.histogram(recommendations['original_price'], bins=price_bins)

    # Generate the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(labels, price_counts, color=plt.cm.tab20.colors[:len(labels)])
    plt.xlabel('Price Brackets')
    plt.ylabel('Number of Games')
    plt.title('Top Recommended Games by Price Bracket')

    # Save the chart as a bytes object
    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format='png')
    plt.close()

    # Convert the bytes object to a base64-encoded string
    chart_data = base64.b64encode(chart_stream.getvalue()).decode('utf-8')

    # Return the chart data as an HTML image tag
    return f'<img src="data:image/png;base64,{chart_data}">'


def createPriceSentimentScatter(recommendations):
    # Count the occurrences of each sentiment
    sentiment_counts = recommendations['review_sentiment'].value_counts()

    # Generate the pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(sentiment_counts, labels=None, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title('Distribution of Review Sentiments')

    # Add a legend
    plt.legend(sentiment_counts.index, loc='upper right')

    # Save the chart as a bytes object
    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format='png')
    plt.close()

    # Convert the bytes object to a base64-encoded string
    chart_data = base64.b64encode(chart_stream.getvalue()).decode('utf-8')

    # Return the chart data as an HTML image tag
    return f'<img src="data:image/png;base64,{chart_data}">'