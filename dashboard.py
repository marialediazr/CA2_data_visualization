#!/usr/bin/env python
# coding: utf-8

# ## Dashboard Maria Diaz

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns
sns.set(color_codes=True)
import chart_studio.plotly as py
import plotly.graph_objs as go
import chardet
from plotly.offline import iplot, init_notebook_mode
import cufflinks
from matplotlib import gridspec
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)
from matplotlib.colors import ListedColormap


# In[2]:


st.set_page_config(
    page_title="Movie Analytics Dashboard",
    layout="wide")

with st.spinner("Loading and processing all datasets..."):
    # Step 1: Detect encoding and load movies dataset
    with open('movies.csv', 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print(result)
    movies = pd.read_csv('movies.csv', encoding='ISO-8859-1')
    movies.to_csv('movies_utf8.csv', index=False, encoding='utf-8')
    movies['year'] = movies['title'].str.extract(r'\((\d{4})\)')

    # Step 2: Load and process ratings dataset
    ratings = pd.read_csv("ratings.csv")

    # Step 3: Detect encoding and load tags dataset
    with open('tags.csv', 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print(result)
    tags = pd.read_csv('tags.csv', encoding='Windows-1252')
    tags.to_csv('tags_utf8.csv', index=False, encoding='utf-8')

st.success("All datasets have been loaded and processed successfully!")
st.text("Let's dive into the visualizations.")


# In[3]:


average_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
average_ratings.columns = ['movieId', 'average_rating']
average_ratings['average_rating'] = average_ratings['average_rating'].round(1)
print(average_ratings)


# def round_to_half(value):
#     return round(value * 2) / 2
# average_ratings['average_rating'] = average_ratings['average_rating'].apply(round_to_half)
# print(average_ratings)

# In[4]:


movies2 = movies.copy()


# In[5]:


movies2 = movies2.merge(average_ratings, on='movieId', how='left')


# In[6]:


movies_graphs = movies2.copy()


# In[7]:


movies2.drop('title', axis=1, inplace=True)


# In[8]:


movies2['year'] = movies2['year'].astype(int)


# In[9]:


st.title("Movie Analytics Dashboard")
st.write("Welcome to the Movie Analytics Dashboard! Dive into interactive charts that reveal movie trends by genre and release year. The dataset features 2,500 films released between 1922 and 2014, with ratings powered by over 90,000 movie enthusiasts. That’s a lot of opinions, so you know we’ve got all the favorites covered! Ready to explore what movies people love the most? Let’s go!")

# Visualization 1: Top 20 Movies by rating
st.header("1. Top 20 Movies by rating")
st.write("This chart highlights the top 20 highest-rated movies ever! It’s proof that classics never go out of style. The oldest film on the list dates back to 1950, while the newest one hit screens in 2011. Drama steals the spotlight with 13 hits, followed by crime with 8, and thriller with 7. Hover over each bar to uncover fun details about these legendary films!")
top_movies = movies_graphs.sort_values(by='average_rating', ascending=False).head(20)
fig_top_movies = px.bar(
    top_movies,
    x='average_rating',
    y='title',
    orientation='h',
    color='genres',
    labels={'average_rating': 'Average Rating', 'title': 'Movie Title', 'genres': 'Genre'},
    title='Top 20 Movies of all time based on rating',
    color_discrete_sequence=px.colors.qualitative.Bold)
fig_top_movies.update_layout(
    height=800,
    title_x=0.0,
    title_font_size=25,
    yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig_top_movies, use_container_width=True)

# Visualization 2: Number of Movies per genre
st.header("2. Number of Movies per genre")
st.write("This chart takes a closer look at how many movies were released in each genre. Drama leads the pack with 1,160 titles—almost half of the entire dataset! Comedy comes in hot with 950 films, while thriller claims the third spot with 639 movies. Hover over each bar to check out more details about your favorite genres!")
df_genres = movies_graphs.copy()
df_genres['genres'] = df_genres['genres'].str.split('|')
df_genres = df_genres.explode('genres')
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Number of Movies']
fig_genres = px.bar(
    genre_counts,
    x="Genre",
    y="Number of Movies",
    title="Number of Movies per genre",
    labels={"Genre": "Movie Genre", "Number of Movies": "Number of Movies"},
    color="Genre",
    color_discrete_sequence=px.colors.qualitative.Bold)
fig_genres.update_layout(
    title_x=0.0,
    title_font_size=25)
st.plotly_chart(fig_genres, use_container_width=True)

# Visualization 3: Movies by year of release and average rating
st.header("3. Movies by year of release and average rating")
st.write("This plot connects the year a movie was released to its average rating. Each dot represents a movie, and you can hover over it to see its name, genre, and rating. Explore and find out which movies stood out in their time!")
movies_graphs['year'] = movies_graphs['year'].astype(int)
fig_year_avg = px.scatter(
    movies_graphs,
    x='year',
    y='average_rating',
    color='genres',
    hover_data=['title'],
    title='Movies by year of release and average rating',
    labels={'year': 'Year', 'average_rating': 'Average Rating', 'genres': 'Genre'},
    color_discrete_sequence=px.colors.qualitative.Bold)
fig_year_avg.update_layout(
    title_x=0.0,
    title_font_size=25)
st.plotly_chart(fig_year_avg, use_container_width=True)

# Visualization 4: Movies released and average rating per year
st.header("4. Movies released and average rating per year")
st.write("One thing’s clear: more movies each year doesn’t always mean better quality. While every year has its standout hits, the average rating started dropping after 1985 as more lower-rated movies hit the screens. Quality over quantity, right?")
movies_per_year = movies2.groupby('year').size()
yearly_avg_rating = movies2.groupby('year')['average_rating'].mean().reset_index()
fig_movies_avg_rating = go.Figure()
fig_movies_avg_rating.add_trace(
    go.Scatter(
        x=movies_per_year.index,
        y=movies_per_year.values,
        mode='lines+markers',
        name='Movies Released',
        line=dict(color='blue', width=2),
        marker=dict(size=6)))
fig_movies_avg_rating.add_trace(
    go.Scatter(
        x=yearly_avg_rating['year'],
        y=yearly_avg_rating['average_rating'],
        mode='lines+markers',
        name='Average Rating',
        line=dict(color='orange', width=2),
        marker=dict(size=6),
        yaxis='y2'))
fig_movies_avg_rating.update_layout(
    title='Movies released and average rating per year',
    title_x=0.0,
    title_font_size=25,
    xaxis=dict(
        title='Year',
        tickmode='array',
        tickvals=list(range(yearly_avg_rating['year'].min(), yearly_avg_rating['year'].max() + 1, 5)),
        tickangle=45),
    yaxis=dict(
        title='Number of Movies',
        gridcolor='lightgray'),
    yaxis2=dict(
        title='Average Rating',
        overlaying='y',
        side='right'),
    template='plotly_white',
    hovermode='x')
st.plotly_chart(fig_movies_avg_rating, use_container_width=True)

# Visualization 5: Changes in genre popularity over the years
st.header("5. Changes in genre popularity over the years")
st.write("This graph is super interesting —it shows how the popularity of genres has shifted over time! Hit the play button to watch how different genres rise and fall in popularity as movies are released over the years.")
movies_expanded = movies_graphs.assign(genres=movies_graphs['genres'].str.split('|')).explode('genres')
all_years = sorted(movies_expanded['year'].unique())
all_genres = sorted(movies_expanded['genres'].unique())
full_grid = pd.DataFrame([(year, genre) for year in all_years for genre in all_genres], columns=['year', 'genres'])
movies_by_genre_year = movies_expanded.groupby(['year', 'genres']).size().reset_index(name='movie_count')
movies_by_genre_year = pd.merge(full_grid, movies_by_genre_year, on=['year', 'genres'], how='left').fillna(0)
movies_by_genre_year['movie_count'] = movies_by_genre_year['movie_count'].astype(int)
fig_genre_popularity = px.bar(
    movies_by_genre_year,
    x='genres',
    y='movie_count',
    color='genres',
    animation_frame='year',
    range_y=[0, movies_by_genre_year['movie_count'].max() + 5],
    labels={'movie_count': 'Number of Movies', 'genres': 'Movie Genre'},
    template='plotly_white')
fig_genre_popularity.update_layout(
    width=1000,
    height=600,
    title={
        'text': '<b>Changes in genres popularity over the years</b>',
        'x': 0.0,
        'xanchor': 'left',
        'yanchor': 'top',
        'font': {'size': 25}},
    xaxis_title='Movie Genre',
    yaxis_title='Number of Movies',
    legend_title='Movie Genre')
st.plotly_chart(fig_genre_popularity, use_container_width=True)

# Visualization 6: Top Movies based on your genre preference
st.header("6. Top Movies based on your genre preference")
st.write("Now it’s your turn! Pick from the dropdown menu your favorite genre and check out the top 20 movies in that category. Have fun exploring!")
movies_df = pd.DataFrame(movies_graphs)
movies_df = movies_df.sort_values(by='average_rating', ascending=False).copy()
unique_genres = set()
movies_df['genres'].str.split('|').apply(unique_genres.update)
unique_genres = sorted(unique_genres)
color_palette = px.colors.qualitative.Bold
genre_colors = {genre: color_palette[i % len(color_palette)] for i, genre in enumerate(unique_genres)}
max_movies_displayed = 20
fig_genre_preference = go.Figure()
for genre in unique_genres:
    filtered_movies = movies_df[movies_df['genres'].str.contains(genre)].copy()
    filtered_movies = filtered_movies.head(max_movies_displayed)
    filtered_movies = filtered_movies[::-1]
    if not filtered_movies.empty:
        fig_genre_preference.add_trace(
            go.Bar(
                x=filtered_movies['average_rating'],
                y=filtered_movies['title'],
                orientation='h',
                name=genre,
                marker=dict(color=genre_colors[genre]),
                visible=False,
                hovertemplate=(
                    '<b>Title:</b> %{y}<br>'
                    '<b>Average Rating:</b> %{x}<br>'
                    '<b>Genres:</b> %{customdata}<extra></extra>'),
                customdata=filtered_movies['genres']))
if fig_genre_preference.data:
    fig_genre_preference.data[0].visible = True
dropdown_buttons_genres = [
    {
        'label': genre,
        'method': 'update',
        'args': [
            {'visible': [trace.name == genre for trace in fig_genre_preference.data]},
            {
                'title': f"<b>Top 20 {genre} Movies based on ratings</b><br><span style='font-size:16px;'>Select the genre you would like to display</span>"}],}
    for genre in unique_genres]
fig_genre_preference.update_layout(
    title="<b>Top 20 Action Movies based on ratings</b><br><span style='font-size:16px;'>Select the genre you would like to display</span>",
    title_x=0.0,
    title_font_size=25,
    xaxis=dict(title='Average Rating', range=[0, 5]),
    yaxis=dict(title='Movie Titles', automargin=True),
    template='plotly_white',
    updatemenus=[
        {
            'buttons': dropdown_buttons_genres,
            'direction': 'down',
            'showactive': True,
            'x': 1.05,
            'xanchor': 'right',
            'y': 1.05,
            'yanchor': 'top'}],
    height=1000,
    width=1000)
st.plotly_chart(fig_genre_preference, use_container_width=True)

# Visualization 7: Top Movies based on the decade
st.header("7. Top Movies based on the decade")
st.write("To wrap things up, we’ve got the top recommendations based on the decade each movie was released. Use the dropdown menu to select a decade and explore the top 20 highest-rated movies from that period. Enjoy the journey through cinematic history!")
movies_decades = movies_graphs.copy()
movies_decades['decade'] = (movies_decades['year'] // 10) * 10
unique_decades = sorted(movies_decades['decade'].unique())
color_palette = px.colors.qualitative.Bold
decade_colors = {decade: color_palette[i % len(color_palette)] for i, decade in enumerate(unique_decades)}
fig_decade_preference = go.Figure()
for decade in unique_decades:
    filtered_movies = movies_decades[movies_decades['decade'] == decade].copy()
    filtered_movies = filtered_movies.sort_values(by='average_rating', ascending=False).head(20)
    filtered_movies = filtered_movies.iloc[::-1]
    fig_decade_preference.add_trace(
        go.Bar(
            x=filtered_movies['average_rating'],
            y=filtered_movies['title'],
            orientation='h',
            name=f"{decade}s",
            marker=dict(color=decade_colors[decade]),
            visible=False,
            hovertemplate=(
                '<b>Title:</b> %{y}<br>'
                '<b>Average Rating:</b> %{x}<br>'
                '<b>Genres:</b> %{customdata[0]}<br>'
                '<b>Decade:</b> %{customdata[1]}<extra></extra>'),
            customdata=list(zip(filtered_movies['genres'], filtered_movies['decade']))))
if fig_decade_preference.data:
    fig_decade_preference.data[0].visible = True
dropdown_buttons_decades = [
    {
        'label': f"{decade}s",
        'method': 'update',
        'args': [
            {'visible': [trace.name == f"{decade}s" for trace in fig_decade_preference.data]},
            {
                'title': f"<b>Top 20 Movies of the {decade}s based on ratings</b><br><span style='font-size:16px;'>Select the decade you would like to display</span>"}],}
    for decade in unique_decades]
fig_decade_preference.update_layout(
    title="<b>Top 20 Movies of the 1920s based on ratings</b><br><span style='font-size:16px;'>Select the decade you would like to display</span>",
    title_x=0.0,
    title_font_size=25,
    xaxis=dict(title='Average Rating', range=[0, 5]),
    yaxis=dict(title='Movie Titles', automargin=True),
    template='plotly_white',
    updatemenus=[
        {
            'buttons': dropdown_buttons_decades,
            'direction': 'down',
            'showactive': True,
            'x': 1.05,
            'xanchor': 'right',
            'y': 1.05,
            'yanchor': 'top'}],
    height=1000)
st.plotly_chart(fig_decade_preference, use_container_width=True)


# In[ ]:




