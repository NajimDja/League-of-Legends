import requests

api_key = "RGAPI-3121abc4-7bd3-45e9-9850-a43a048de154"

class Extract:

    def get_puuid(self, gameName : str, tagLine : str):
        requete = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"