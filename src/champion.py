import requests
import json

class ExtractChampionData:

    def get_latest_version(self):
        versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
        latest = versions[0]
        print(latest)

    def get_all_champion(self):
        url = "https://ddragon.leagueoflegends.com/cdn/16.4.1/data/fr_FR/champion.json"
        resp = requests.get(url).json()
        print(resp)
        return resp
    
    def get_image_champion(self):
        url = "https://ddragon.leagueoflegends.com/cdn/16.4.1/img/champion/Aatrox.png"
        resp = requests.get(url)
        with open(r"C:\Users\najim\Documents\Projets\LeagueOfLegends\images\Aatrox.png", "wb") as file:
            file.write(resp.content)

ExtractChampionData().get_latest_version()
# ExtractChampionData().get_all_champion()
# ExtractChampionData().get_image_champion()