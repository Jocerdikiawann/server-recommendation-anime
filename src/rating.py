import pandas as pd


class Rating:
    def __init__(self) -> None:
        pass

    def addRating(self, user_id, anime_id, rating):
        # Generate user
        new_user = pd.DataFrame({
            "user_id": user_id,
            "anime_id": [anime_id],
            "rating": [rating]
        })

        return new_user
