import requests
import time
import re
from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import json
from keys_data import KeysData
load_dotenv()

api_key = os.getenv("API_KEY")
# Limit
# 20 requests evry 1 seconds
# 100 requests every 2 minutes

class ExtractPlayerData:

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


    def get_all_games_ids(self, puuid: str, count_per_request: int = 100, delay: float = 1.5) -> list:
        """
        Récupère l'ensemble des IDs de parties d'un joueur via pagination.
        
        Args:
            puuid: Identifiant unique du joueur
            count_per_request: Nombre de résultats par requête (max 100 selon l'API Riot)
            delay: Délai en secondes entre chaque requête (adapter selon votre clé API)
        
        Returns:
            List[str]: Liste complète des IDs de toutes les parties jouées
        """
        all_match_ids = []
        start = 0

        while True:
            api_url = (
                f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
                f"{puuid}/ids?start={start}&count={count_per_request}&api_key={api_key}"
            )

            try:
                response = requests.get(api_url)

                # Gestion du rate limiting (429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 10))
                    print(f"\t-Rate limit atteint. Attente de {retry_after}s...")
                    time.sleep(retry_after)
                    continue  # Rejoue la même requête

                response.raise_for_status()
                batch = response.json()

            except requests.exceptions.RequestException as e:
                print(f"\t-Erreur lors de la requête (start={start}) : {e}")
                break

            if not batch:
                break  # Plus de résultats, pagination terminée

            all_match_ids.extend(batch)
            print(f"\t- {len(all_match_ids)} parties récupérées...")

            # Si le batch est incomplet, c'est la dernière page
            if len(batch) < count_per_request:
                break

            start += count_per_request
            time.sleep(delay)  # Respect du rate limit entre les requêtes

        return all_match_ids


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
    
    
    def get_challenges_description(self, challenge_id : int):
        """Returns the description of a challenge"""

        api_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/challenges/{challenge_id}/config?api_key={api_key}"
        resp = requests.get(api_url).json()
        return resp
    

class TransformPlayerData:

    def _dict_to_list_dict(self, dico : dict) -> list[dict]:
        """Ajoute un dico à une liste"""
        return [dico]
    
    def to_dataframe(self, data) -> pd.DataFrame:
        """Convertie des données de forme dict ou list[dict] en dataframe"""
        if type(data) == dict:
            data = self._dict_to_list_dict(data)
        return pd.DataFrame(data)
    
    def drop_col(self, df : pd.DataFrame, cols : list) -> pd.DataFrame:
        """Enlève des colonnes du dataframe"""
        return df.drop(columns=cols)

    def rename_df_cols(self, df : pd.DataFrame, renamer : dict) -> pd.DataFrame:
        """Rename des colonnes avec un dico {old_col_name : new_col_name}"""
        return df.rename(columns=renamer)
    
    def format_timestamp(self, df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
        """Formatage des colonnes listées en timestamp au format yyyy-mm-dd hh:mm:ss"""
        for col in cols:
            df[col] = pd.to_datetime(df[col], unit="ms").dt.floor("s")
        return df
    
    def add_puuid(self, df : pd.DataFrame, puuid : str) -> pd.DataFrame:
        """Ajoute le puuid du joueur à un dataframe"""
        df['puuid'] = puuid
        return df
    
    def map_catg_with_index(self, df : pd.DataFrame, col_to_map : str, name_map :str, mapper : dict) -> pd.DataFrame:
        """Ajoue une nouvelle colonne en mappant avec un dico de correspondance"""
        df[name_map] = df[col_to_map].map(mapper)
        return df
    
    def drill_down_dico(self, dico: dict, **kwargs):
        result = dico
        for key, value in kwargs.items():
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                raise KeyError(f"Key '{key}' not found in dict")
        return result
    
    def add_key(self, dico : dict, new_key_val : dict):
        """Ajoute des pairs {clé : valeur} à un dictionnaire"""
        dico.update(new_key_val)
        return dico
    
    def clean_text(self, txt : str, exp : str, sub : str):
        """Remplace des éléments de texte spécifiques"""
        txt = re.sub(exp, sub, txt)
        return txt
    
    def merge_df(self, df1 : pd.DataFrame, df2 : pd.DataFrame, left_key : list[str], rigth_key : list[str], how : str = 'inner'):
        """Execute une jointure en deux dataframes"""
        df_merge = pd.merge(df1, df2, how=how, left_on=left_key, right_on=rigth_key)
        return df_merge
    
    def sec_to_minsec(self, secondes : int):
        """Convertie des secondes en format minute:secondes"""
        minu = secondes//60
        sec = secondes%60
        txt = f"{minu:02d}:{sec:02d}"
        return txt
    
    def add_underscore(self, col_names: list[str]) -> list[str]:
        """Convertit les noms de colonnes en snake_case (gestion avancée des majuscules)."""
        def camel_to_snake(name: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name) # Insère _ avant les majuscules précédées de minuscules ou chiffres
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() # Insère _ avant les majuscules suivies de minuscules
        
        return [camel_to_snake(name) for name in col_names]
    

class Pipelines:

    def __init__(self):
        self.extract = ExtractPlayerData()
        self.transfo = TransformPlayerData()
        self.keys_data = KeysData()


    def pipeline_account(self, gameName : str, tagLine : str):
        """Récupération et traitement des données de compte"""

        print(f"- Récupération du puuid du joueur {gameName} (#{tagLine}).")
        df_account = self.extract.get_puuid(gameName=gameName, tagLine=tagLine)
        puuid = df_account['puuid']
        df_account = self.transfo.to_dataframe(data=df_account)
        df_account = self.transfo.rename_df_cols(df_account, renamer = {'gameName':'game_name', 'tagLine':'tag_line'})
        return df_account, puuid


    def pipeline_summoner(self, puuid : str) -> pd.DataFrame:
        """Récupération et traitement des données du summoner"""

        print("- Récupération des données du summoner du joueur.")
        df_summoner = self.extract.get_summoner_info(puuid=puuid)
        df_summoner = self.transfo.to_dataframe(data=df_summoner)
        df_summoner = self.transfo.rename_df_cols(df_summoner, renamer = {'profileIconId':'profile_icon_id', 
                                                                          'revisionDate':'last_modif', 
                                                                          'summonerLevel':'summoner_level'})
        df_summoner = self.transfo.format_timestamp(df_summoner, cols=['last_modif'])
        return df_summoner


    def pipeline_challenges(self, puuid : str) -> pd.DataFrame:
        """Récupération et traitement des données de challenges"""

        print("- Récupération des données d'avancement de challenges du joueur.")
        df_challenges = self.extract.get_challenges_info(puuid=puuid)['challenges']
        df_challenges = self.transfo.to_dataframe(df_challenges)
        df_challenges = self.transfo.format_timestamp(df_challenges, cols = ["achievedTime"])
        df_challenges = self.transfo.drop_col(df_challenges, cols=['position','playersInLevel'])
        df_challenges = self.transfo.rename_df_cols(df_challenges, renamer={'challengeId':'challenge_id', 'achievedTime':'achieved_time'})
        df_challenges = self.transfo.map_catg_with_index(df_challenges, col_to_map='level', name_map='level_index', 
                                                    mapper={'NONE' : 0, 'IRON' : 1, 'BRONZE' : 2, 'SILVER' : 3, 'GOLD' : 4, 
                                                            'PLATINUM' : 5, 'DIAMOND' : 6, 'MASTER' : 7, 'GRANDMASTER' : 8, 'CHALLENGER' : 9})
        all_challenge = []
        cnt = 0
        for id in df_challenges['challenge_id']:
            resp = self.extract.get_challenges_description(challenge_id=id)
            chall_id = self.transfo.drill_down_dico(dico=resp, id='id')
            chall_desc = self.transfo.drill_down_dico(dico=resp, localizedNames="localizedNames", fr_FR="fr_FR")
            chall_desc = self.transfo.add_key(dico=chall_desc, new_key_val={'challenge_id':chall_id})
            all_challenge.append(chall_desc)
            cnt += 1
            print(f"\t- Requete challenges envoyées : {cnt}", end='\r')
            time.sleep(1.5)
        
        all_challenge = self.transfo.to_dataframe(all_challenge)
        all_challenge = self.transfo.drop_col(all_challenge, cols=['shortDescription'])
        all_challenge['description'] = [self.transfo.clean_text(txt=x, exp=r"\xa0", sub="") for x in all_challenge['description']]
        all_challenge['name'] = [self.transfo.clean_text(txt=x, exp=r"\xa0", sub="") for x in all_challenge['name']]
        
        df = self.transfo.merge_df(df1=df_challenges, df2=all_challenge, left_key=['challenge_id'], rigth_key=['challenge_id'], how='left')
        df = self.transfo.add_puuid(df, puuid=puuid)
        return df


    def pipeline_champion_mastery(self, puuid : str) -> pd.DataFrame:
        """Récupération et traitement des données de maitrise des champions"""

        print("- Récupération des données de maîtrise de champions du joueur.")
        df_champion_mastery = self.extract.get_champion_mastery(puuid=puuid)
        df_champion_mastery = self.transfo.to_dataframe(df_champion_mastery)
        df_champion_mastery = self.transfo.drop_col(df_champion_mastery, cols=['championPointsSinceLastLevel', 'markRequiredForNextLevel',
                                                                        'tokensEarned', 'championSeasonMilestone', 'milestoneGrades', 
                                                                        'nextSeasonMilestone'])
        df_champion_mastery = self.transfo.format_timestamp(df_champion_mastery, cols = ['lastPlayTime'])
        df_champion_mastery = self.transfo.rename_df_cols(df_champion_mastery, renamer={'championId':'champ_id', 'championLevel':'champ_level',
                                                                                'championPoints':'champ_points', 'lastPlayTime':'last_time_played',
                                                                                'championPointsUntilNextLevel':'points_to_next_level'})
        return df_champion_mastery
    
    
    def pipeline_queue(self, puuid : str) -> pd.DataFrame:
        """Récupération et traitement des données de ranked"""

        print("- Récupération des données de queue (ranked)")
        df_queue = self.extract.get_gamer_queue(puuid=puuid)
        df_queue = self.transfo.to_dataframe(df_queue)
        df_queue = self.transfo.drop_col(df_queue, cols=['veteran', 'inactive', 'freshBlood', 'hotStreak'])
        df_queue = self.transfo.rename_df_cols(df_queue, renamer={'leagueId':'league_id', 'queueType':'queue_type', 'leaguePoints':'league_points'})
        return df_queue
    

    def pipeline_games(self, puuid : str):
        """Récupération et traitement des données de parties"""

        print("- Récupération des données de parties de jeux.")
        
        df_matchs_info = []

        list_id_games = self.extract.get_all_games_ids(puuid=puuid)
        
        # p = [puuid for x in list_id_games]
        # df_gameid_puuid = pd.DataFrame({'game_id': list_id_games, 'puuid': p})

        for id in list_id_games:
            
            game = self.extract.get_game_data(game_id=id)

            index_player = game['metadata']['participants'].index(puuid)
            
            game_info = game['info']
            game_info = {k:v for k,v in game.items() if k in self.keys_data.keys_match_info}
            game_info.update({'match_id' : id, 'puuid' : puuid})

            game_data = game['info']['participants'][index_player]
            
            df_matchs_info.append(game_info)

        df_matchs_info = self.transfo.to_dataframe(df_matchs_info) #.drop(columns=['gameId'])
        df_matchs_info.columns = self.transfo.add_underscore(col_names = df_matchs_info.columns)

        return df_matchs_info
    

def pipeline_new_player(gameName : str, tagLine : str):
    """Insérer un nouveau joueur en base."""
    
    pipe = Pipelines()

    df_account, puuid = pipe.pipeline_account(gameName=gameName, tagLine=tagLine)
    df_summoner = pipe.pipeline_summoner(puuid=puuid)
    df_challenges = pipe.pipeline_challenges(puuid=puuid)
    df_champion_mastery = pipe.pipeline_champion_mastery(puuid=puuid)
    df_queue = pipe.pipeline_queue(puuid=puuid)

    return df_account, df_summoner, df_challenges, df_champion_mastery, df_queue