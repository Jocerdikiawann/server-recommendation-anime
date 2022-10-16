import pandas as pd


class Database:

    def __init__(self, path_rating, path_anime_info) -> None:
        self.rating_user = pd.read_csv(path_rating)
        self.anime_info = pd.read_csv(path_anime_info)
        self.anime_info = self.anime_info[self.anime_info.columns[1:]]
        self.rating_user = self.rating_user[self.rating_user.columns[1:]]

    def getDbRatingUser(self):
        return self.rating_user

    def getDbAnimeInfo(self):
        return self.anime_info
