from src.database import Database
from src.rating import Rating
from src.recommender import Recommender
from src.anime import Anime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = Database("./data/rating.csv", './data/clean_anime.csv')
user_id = (len(db.rating_user.user_id.unique()) + 1)


@app.route('/')
def hello_flask():
    print(f"panjang user : {user_id}")

    return jsonify({
        "code": 200,
        "status": "ok",
        "message": "welcome",
        "data": "Hallo"
    })


@app.route("/anime", methods=['GET'])
def getTourism():
    size = int(request.args.get("size"))
    data, totalOfSize = Anime().getAnime(db=db.anime_info, size=size)

    return jsonify({
        "code": 200,
        "status": "ok",
        "message": "welcome",
        "data": {
            "totalOfSize": totalOfSize,
            "items": data
        }
    })


@app.route("/rating", methods=['POST'])
def addRating():
    request_data = request.get_json()

    rating = Rating().addRating(
        user_id,
        request_data['anime_id'],
        request_data['rating'])

    db.rating_user = db.rating_user.append(rating)
    return jsonify({
        "code": 201,
        "status": "ok",
        "message": "welcome",
        "data": db.rating_user[db.rating_user.user_id == user_id].to_dict('records')
    })


@app.route("/rating", methods=['GET'])
def getRatingByUser():
    return jsonify({
        "code": 200,
        "status": "ok",
        "message": "welcome",
        "data": db.rating_user[db.rating_user.user_id == user_id].to_dict('records')
    })


@app.route('/recommend', methods=['GET'])
def recommend():
    top_anime_user, top_n_recommendation = Recommender().processing(
        "http://localhost:8501/v1/models/rps_model:predict",
        db.rating_user,
        db.anime_info,
        user_id)

    return jsonify({
        "code": 200,
        "status": "ok",
        "message": "welcome",
        "data": {
            "high_rating_by_user": top_anime_user.to_dict('records'),
            "top_n_recommendation": top_n_recommendation.to_dict("records")
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=3000)
