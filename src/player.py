import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import json
load_dotenv()

api_key = os.getenv("API_KEY")
# Limit
# 20 requests evry 1 seconds
# 100 requests every 2 minutes


class Extract:

    def get_puuid(self, gameName : str, tagLine : str):
        """Get account by riot id  
        Returns :
        - puuid : Encrypted PUUID. Exact length of 78 characters.
        - gameName : Name of the account
        - tagLine : Indicatif of the account
        """
        api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp

    def get_summoner_info(self, puuid : str):
        """Get a summoner general information by PUUID  
        Returns :
        - profileiconId : ID of the summoner icon associated with the summoner.
        - revisionDate : last modification (events : profile icon change, playing tuto, finishing a game, summoner name change).
        - puuid : Encrypted PUUID. Exact length of 78 characters.
        - summonerLevel : Summoner level associated with the summoner.
        """

        api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

    def get_last_games_ids(self, puuid :str, start : int = 0, count : int = 20):
        """Get a list of match ids by puuid
        Returns :
        - List : List of last matches
        """

        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

    def get_game_data(self, game_id : str):
        """Get all informations of a match by match id"""

        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{game_id}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

    def get_champion_mastery(self, puuid : str):
        """Get all champion mastery entries sorted by number of champion points descending."""

        api_url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

    def get_gamer_queue(self, puuid : str):
        """Get league entries in all queues for a given puuid"""
    
        api_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

    def get_challenges_info(self, puuid : str):
        """Returns player information with list of all progressed challenges (REST)"""

        api_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/player-data/{puuid}?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp