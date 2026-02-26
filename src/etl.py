import requests

api_key = "RGAPI-3121abc4-7bd3-45e9-9850-a43a048de154"

class Extract:

    def get_puuid(self, gameName : str, tagLine : str):
        api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
        resp = requests.get(api_url)
        resp = resp.json()
        puuid = resp['puuid']
        return puuid

    def get_summoner_info(self, puuid : str):
        api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
        resp = requests.get(api_url)
        resp = resp.json()
        return resp
    
    def get_last_games_ids(self, puuid :str, start : int = 0, count : int = 20):
        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}"
        resp = requests.get(api_url)
        resp = resp.json()
        return resp
    
    def get_game_data(self, game_id : str):
        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game_id}?api_key={api_key}"
        resp = requests.get(api_url)
        resp = resp.json()
        return resp