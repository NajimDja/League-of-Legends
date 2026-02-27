import requests
import json

class ExtractChampionData:

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

# ExtractChampionData().get_all_champion()
ExtractChampionData().get_image_champion()