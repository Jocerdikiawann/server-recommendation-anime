import numpy as np
import requests


class Recommender:

    def __init__(self):
        pass

    def processing(self, endpoint, db_rating, db_anime_info, user_id):

        anime_to_anime_encoded = {x: i for i, x in enumerate(
            db_anime_info.anime_id.unique().tolist())}

        anime_encoded_to_anime = {x: i for x, i in enumerate(
            db_anime_info.anime_id.unique().tolist())}

        user_to_user_encoded = {x: i for i, x in enumerate(
            db_rating.user_id.unique().tolist())}

        anime_watched_by_user = db_rating[db_rating.user_id == user_id]

        anime_not_watched = db_anime_info[~db_anime_info['anime_id'].isin(
            anime_watched_by_user['anime_id'].values)]['anime_id']

        anime_not_watched = list(
            set(anime_not_watched)
            .intersection(set(anime_to_anime_encoded.keys()))
        )

        anime_not_watched = [
            [anime_to_anime_encoded.get(x)] for x in anime_not_watched]

        user_encoder = user_to_user_encoded.get(user_id)

        payload = {
            "instances": np.hstack(
                ([[user_encoder]] * len(anime_not_watched),
                 anime_not_watched)
            ).tolist()
        }

        response = requests.post(endpoint, json=payload)

        ratings = np.array(response.json()['predictions']).flatten()

        top_anime_user = (
            anime_watched_by_user.sort_values(
                by='rating',
                ascending=False
            )
            .head(5)
            .anime_id.values
        )

        top_ratings_indices = ratings.argsort()[-10:][::-1]

        recommended_anime_ids = [
            anime_encoded_to_anime.get(anime_not_watched[x][0]) for x in top_ratings_indices
        ]

        high_rating_user_watched = db_anime_info[db_anime_info['anime_id'].isin(
            top_anime_user)]

        top_n_recommendation = db_anime_info[db_anime_info['anime_id'].isin(
            recommended_anime_ids)]

        return high_rating_user_watched, top_n_recommendation
