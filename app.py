from flask import Flask, render_template, request, jsonify
import pickle
import requests

app = Flask(__name__)


OMDB_API_KEY = "f0dc7216"

holly_df = pickle.load(open("model/hollywood.pkl", "rb"))
holly_similarity = pickle.load(open("model/similarity_hly.pkl", "rb"))

bolly_df = pickle.load(open("model/bollywood.pkl", "rb"))
bolly_similarity = pickle.load(open("model/similarity_bly.pkl", "rb"))


# OMDB POSTER FETCH
def fetch_poster_omdb(movie_title):
    try:
        url = f"https://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        poster = data.get("Poster")

        if poster and poster != "N/A":
            return poster

    except requests.exceptions.RequestException:
        pass

    return None



# PAGES
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/hollywood")
def hollywood_page():
    return render_template("hollywood.html")


@app.route("/bollywood")
def bollywood_page():
    return render_template("bollywood.html")



# MOVIE LIST (FOR DROPDOWNS)
@app.route("/hollywood/movies")
def hollywood_movies():
    return jsonify(sorted(holly_df["title"].unique().tolist()))


@app.route("/bollywood/movies")
def bollywood_movies():
    return jsonify(sorted(bolly_df["movie_name"].unique().tolist()))


# HOLLYWOOD RECOMMENDATION
@app.route("/hollywood/recommend")
def hollywood_recommend():
    movie = request.args.get("movie")

    if not movie:
        return jsonify({"error": "Movie name required"})

    try:
        movie_index = holly_df[holly_df["title"] == movie].index[0]
        distances = holly_similarity[movie_index]

        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:21]

        results = []
        for i in movies_list:
            title = holly_df.iloc[i[0]].title
            poster = fetch_poster_omdb(title)

            results.append({
                "title": title,
                "poster": poster
            })

        return jsonify(results)

    except IndexError:
        return jsonify({"error": "Movie not found"})


# BOLLYWOOD RECOMMENDATION
@app.route("/bollywood/recommend")
def bollywood_recommend():
    movie = request.args.get("movie")

    if not movie:
        return jsonify({"error": "Movie name required"})

    try:
        movie_index = bolly_df[bolly_df["movie_name"] == movie].index[0]
        distances = bolly_similarity[movie_index]

        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:31]

        results = []
        for i in movies_list:
            title = bolly_df.iloc[i[0]].movie_name
            poster = fetch_poster_omdb(title)

            results.append({
                "title": title,
                "year": int(bolly_df.iloc[i[0]].year),
                "poster": poster
            })

        return jsonify(results)

    except IndexError:
        return jsonify({"error": "Movie not found"})



# BOLLYWOOD (NAVBAR)
@app.route("/bollywood/search/genre")
def search_genre():
    genre = request.args.get("genre")

    result = bolly_df[bolly_df["genre"].apply(
        lambda x: genre.lower() in " ".join(x).lower()
    )].head(30)

    response = []
    for _, row in result.iterrows():
        response.append({
            "title": row["movie_name"],
            "year": int(row["year"]),
            "poster": fetch_poster_omdb(row["movie_name"])
        })

    return jsonify(response)


@app.route("/bollywood/search/year")
def search_year():
    year = request.args.get("year")
    if not year or not year.isdigit():
        return jsonify([])

    year = int(year)
    result = bolly_df[bolly_df["year"] == year].head(30)

    response = []
    for _, row in result.iterrows():
        response.append({
            "title": row["movie_name"],
            "year": int(row["year"]),
            "poster": fetch_poster_omdb(row["movie_name"])
        })

    return jsonify(response)

@app.route("/bollywood/search/director")
def search_director():
    name = request.args.get("name")

    result = bolly_df[bolly_df["director"].apply(
        lambda x: name.lower() in " ".join(x).lower()
    )].sort_values(by="year", ascending=False).head(30)

    response = []
    for _, row in result.iterrows():
        response.append({
            "title": row["movie_name"],
            "year": int(row["year"]),
            "poster": fetch_poster_omdb(row["movie_name"])
        })

    return jsonify(response)


@app.route("/bollywood/search/actors")
def search_actors():
    name = request.args.get("name")

    result = bolly_df[bolly_df["actors"].apply(
        lambda x: name.lower() in " ".join(x).lower()
    )].head(30)

    response = []
    for _, row in result.iterrows():
        response.append({
            "title": row["movie_name"],
            "year": int(row["year"]),
            "poster": fetch_poster_omdb(row["movie_name"])
        })

    return jsonify(response)




if __name__ == "__main__":
    app.run(debug=True)
