class Anime:

    def __init__(self) -> None:
        pass

    def getAnime(self, db, size):
        json_data = db[:size].to_dict('records')
        totalOfSize = len(db)
        return json_data, totalOfSize
