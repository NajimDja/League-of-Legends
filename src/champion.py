import requests
import json

class ExtractChampionData:

    def __init__(self):
        self.last_version = self.get_latest_version()

    def get_latest_version(self):
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        rep = requests.get(url).json()
        latest = rep[0]
        return latest

    def get_all_champion(self):
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/data/fr_FR/champion.json"
        resp = requests.get(url).json()
        print(resp)
        return resp
    
    def get_image_champion(self):
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/img/champion/Aatrox.png"
        resp = requests.get(url)
        with open(r"C:\Users\najim\Documents\Projets\LeagueOfLegends\images\Aatrox.png", "wb") as file:
            file.write(resp.content)

ExtractChampionData().get_latest_version()
# ExtractChampionData().get_all_champion()
# ExtractChampionData().get_image_champion()