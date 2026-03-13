import requests
import numpy as np
import pandas as pd
import re
import os

class ExtractChampionData:

    def __init__(self):
        self.last_version = self.get_latest_version()
        self.list_champ = self.get_all_champ_general_data()
        self.list_champ = list(self.list_champ.keys())

    def get_latest_version(self):
        """Get the last version of the game"""
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        rep = requests.get(url).json()
        latest = rep[0]
        return latest

    def get_all_champ_general_data(self):
        """Get the champion data"""
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/data/fr_FR/champion.json"
        resp = requests.get(url).json()
        return resp['data']
    
    def get_details_champ_data(self):
        """Get detail champion data"""
        data = []
        for champ in self.list_champ:
            url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/data/fr_FR/champion/{champ}.json"
            resp = requests.get(url).json()['data']
            data.append(resp[champ])
        return data
    
    def get_runes(self):
        """Get the runes data"""
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/data/fr_FR/runesReforged.json"
        resp = requests.get(url).json()
        return resp

    # def download_all_png_champion(self):
    #     """Download all champions pictures"""
    #     for champ in self.list_champ:
    #         url = f"https://ddragon.leagueoflegends.com/cdn/{self.last_version}/img/champion/{champ}.png"
    #         path_save = fr"C:\Users\najim\Documents\Projets\LeagueOfLegends\images\{champ}.png"

    #         resp = requests.get(url)
    #         with open(path_save, "wb") as file:
    #             file.write(resp.content)

class TransformChampionData:

    def __init__(self):
        self.keys_to_drop = ['image', 'skins', 'blurb']
        self.table_champion = ['key', 'name', 'title', 'lore', 'tags', 'partype']
        self.table_champ_passive = ['key', 'passive']
        self.table_champ_info = ['key', 'info', 'allytips', 'enemytips']
        self.table_champ_spells = ['key', 'spells']
        self.table_champ_stats = ['key', 'stats']
    
    def drop_keys(self, data : list) -> list:
        new_data = []
        for dict_champ in data:
            dict_champ = {k: v for k,v in dict_champ.items() if k not in self.keys_to_drop}
            new_data.append(dict_champ)
        return new_data
    
    def dispatch_data(self, data : list):
        table_champion = []
        table_champ_passive = []
        table_champ_info = []
        table_champ_spells = []
        table_champ_stats = []
        
        for dict_champ in data:
            champion = {k: v for k,v in dict_champ.items() if k in self.table_champion}
            champ_passive = {k: v for k,v in dict_champ.items() if k in self.table_champ_passive}
            champ_info = {k: v for k,v in dict_champ.items() if k in self.table_champ_info}
            champ_spells = {k: v for k,v in dict_champ.items() if k in self.table_champ_spells}
            champ_stats = {k: v for k,v in dict_champ.items() if k in self.table_champ_stats}

            table_champion.append(champion)
            table_champ_passive.append(champ_passive)
            table_champ_info.append(champ_info)
            table_champ_spells.append(champ_spells)
            table_champ_stats.append(champ_stats)
            
        return table_champion, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats
    
    def split_stats(self, data : list):
        stats_cst, stats_up = [], []
        for stat in data:
            cst = {k:v for k,v in stat.items() if "perlevel" not in k}
            up = {k: v for k, v in stat.items() if "perlevel" in k or "key" in k}
            stats_cst.append(cst)
            stats_up.append(up)
        return stats_cst, stats_up

    def listing_into_text(self, data : list, key : str, sep : str = " "):
        new_data = []
        for champ in data:
            new_value = f"{sep}".join(champ[key])
            champ[key] = self._clean_text(new_value)
            new_data.append(champ)
        return new_data

    def dict_into_first_level(self, data : list, key_to_flat : str) -> list:
        new_data = []
        for champ in data:
            base = {k: v for k, v in champ.items() if k != key_to_flat}
            base.update(champ.get(key_to_flat, {}))
            new_data.append(base)
        return new_data
    
    def pop_key(self, data : list, key_to_remove : list[str]) -> list:
        new_data = []
        for i in data:
            for key in key_to_remove:
                d = i.pop(key, None)
            new_data.append(i)
        return new_data
    
    def _clean_text(self, desc : str) -> str:
        desc = re.sub(r"<[^>]+>|<[a-z]>", " ", desc)
        desc = re.sub(r"\xa0", " ", desc)
        desc = re.sub(r"_ClientTooltipWrapper|Wrapper", "", desc)
        desc = re.sub(r"\{\{.*?\}\}", "XX", desc)
        desc = re.sub(r"XX$", "", desc)
        desc = re.sub(r"[ ]+", " ", desc)
        return desc

    def text_cleaning(self, data : list, key : str) -> list:
        clean = []
        for champ in data:
            desc = self._clean_text(champ[key])
            champ[key] = desc
            clean.append(champ)
        return clean
    
    def rename_cols(self, df : pd.DataFrame, rename : dict) -> pd.DataFrame:
        return df.rename(columns=rename)

    def clean_spells_data(self, data: list):
        new_data = []
        for champ in data:
            idchamp = champ['key']
            spells = champ['spells']

            spells = self.pop_key(
                spells,
                key_to_remove=['leveltip', 'description', 'cooldown', 'cost', 'datavalues',
                    'effect', 'vars', 'image', 'effectBurn', 'range', 'resource'])

            spells_clean = self.text_cleaning(spells, 'tooltip')
            spells_clean = self.text_cleaning(spells, 'name')
            spells_clean = self.text_cleaning(spells, 'id')

            for spell in spells_clean:
                spell['key'] = idchamp
                new_data.append(spell)

        return new_data
    
    def correct_spell_name(self, df_spells : pd.DataFrame, df_champ : pd.DataFrame) -> pd.DataFrame:
        """Rectifie les noms des spells de chaque champion"""

        df_spells = df_spells.rename(columns={'name':'spell_name'})
        df_merge = pd.merge(df_spells, df_champ[['key', 'name']], on='key')
        letters = ['Q', 'W', 'E', 'R']

        # numérotation 0,1,2,3 par groupe de 'name'
        df_merge['spell_rank'] = df_merge.groupby('name').cumcount()
        # on mappe 0→Q, 1→W, 2→E, 3→R
        df_merge['spell_id'] = df_merge['name'] + df_merge['spell_rank'].map(lambda x: letters[x])
        df_merge['spell_rank'] = df_merge['spell_rank'] + 1
        df_merge = df_merge.drop(columns=['name', 'id'])
        df_merge = df_merge.rename(columns={'key':'champ_id'})
        df_merge = df_merge[['champ_id', 'spell_id', 'spell_name', 'tooltip', 'maxrank', 'cooldownBurn', 'costBurn', 
                             'costType', 'maxammo', 'rangeBurn', 'spell_rank', 'patch_id']]
        return df_merge
        
    def correct_spell_costype(self, df_spells : pd.DataFrame, df_champ : pd.DataFrame) -> pd.DataFrame:
        """Rectifie les resources consommées de chaque spells"""

        df_merge = pd.merge(df_spells, df_champ[['key', 'partype']], left_on='champ_id', right_on='key')

        df_merge['costType'] = df_merge['costType'].str.strip()

        df_merge['costType'] = np.where(
            df_merge['costType'] == r"{{ abilityresourcename }}", 
            df_merge['partype'], 
            df_merge['costType'])
        
        expression = r"\(?\{\{.*?\}\}\)?|\+|\."
        df_merge["costType"] = df_merge["costType"]\
            .str.replace(expression, "", regex=True)\
            .str.replace(r"\s+", ' ', regex=True)\
            .str.lower()

        return df_merge.drop(columns=['key', 'partype'])

    def transform_to_df(self, data : list, version : str) -> pd.DataFrame:
        """Transforme une liste de dictionnaire en dataframe pandas"""
        data = pd.DataFrame(data)
        data['patch_id'] = int(re.sub(r'[^0-9]', "", version))
        return data
    
    def transform_runes(self, data : list, version : str) -> pd.DataFrame:
        """Récupérer les runes et transforme en dataframe pandas"""
        df_runes = pd.DataFrame(data)\
            .drop(columns=['icon', 'key'])\
            .rename(columns={'id' : 'type_rune_id', 'name':'type_name'})
        
        df_slots = df_runes.explode('slots').reset_index(drop=True)

        df_slots = pd.concat([
            df_slots.drop(columns=['slots']), 
            pd.json_normalize(df_slots['slots'])], 
            axis=1)

        df_runes = df_slots.explode('runes').reset_index(drop=True)
        
        df_runes = pd.concat([
            df_runes.drop(columns=['runes']), 
            pd.json_normalize(df_runes['runes'])], 
            axis=1)
        
        df_runes = df_runes\
            .rename(columns={'id':'child_rune_id', 'longDesc' : 'description'})\
            .drop(columns=['icon', 'key', 'shortDesc'])
        
        df_runes['description'] = [self._clean_text(x).strip() for x in df_runes['description']]
        df_runes['patch_id'] = re.sub(r"[^0-9]", "", version)
        
        return df_runes


def pipeline_champion():
    """Pipeline d'application des méthodes d'extraction, de transformation et de chargement"""
    
    extract = ExtractChampionData()
    lastest_version = extract.last_version
    print("Lastest version :", lastest_version)
    transform = TransformChampionData()

    details = extract.get_details_champ_data()
    table_runes = extract.get_runes()
    details = transform.drop_keys(details)
    
    table_champion, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats = transform.dispatch_data(details)

    
    table_champion = transform.listing_into_text(table_champion, "tags", sep=' / ')
    table_champion = transform.text_cleaning(table_champion, key='lore')
    table_champion = transform.text_cleaning(table_champion, key='title')
    
    table_champ_info = transform.listing_into_text(table_champ_info, key="enemytips", sep=' ')
    table_champ_info = transform.listing_into_text(table_champ_info, key="allytips", sep=' ')
    table_champ_info = transform.dict_into_first_level(table_champ_info, key_to_flat='info')

    table_champ_passive = transform.dict_into_first_level(table_champ_passive, key_to_flat='passive')
    table_champ_passive = transform.pop_key(table_champ_passive, key_to_remove=['image'])
    table_champ_passive = transform.text_cleaning(table_champ_passive, key='name')
    table_champ_passive = transform.text_cleaning(table_champ_passive, key='description')

    table_champ_stats = transform.dict_into_first_level(table_champ_stats, key_to_flat='stats')
    table_champ_stats, table_champ_stats_up = transform.split_stats(table_champ_stats)

    table_champ_spells = transform.clean_spells_data(table_champ_spells)

    table_champion = transform.transform_to_df(table_champion, version=lastest_version)
    table_champ_info = transform.transform_to_df(table_champ_info, version=lastest_version)
    table_champ_passive = transform.transform_to_df(table_champ_passive, version=lastest_version)
    table_champ_stats = transform.transform_to_df(table_champ_stats, version=lastest_version)
    table_champ_stats_up = transform.transform_to_df(table_champ_stats_up, version=lastest_version)
    table_champ_spells = transform.transform_to_df(table_champ_spells, version=lastest_version)

    table_champ_spells = transform.correct_spell_name(table_champ_spells, table_champion)
    table_champ_spells = transform.correct_spell_costype(table_champ_spells, table_champion)

    table_champion_version = table_champion[['key', 'title', 'lore', 'tags', 'partype', 'patch_id']]
    table_champion = table_champion[['key', 'name']]

    table_runes = transform.transform_runes(table_runes, version=lastest_version)

    table_champion = transform.rename_cols(table_champion, rename={'key':'id'})
    table_champion_version = transform.rename_cols(table_champion_version, rename={'key':'champ_id'})
    table_champ_info = transform.rename_cols(table_champ_info, rename={'key':'champ_id'})
    table_champ_passive = transform.rename_cols(table_champ_passive, rename={'key':'champ_id'})
    table_champ_stats = transform.rename_cols(table_champ_stats, rename={'key':'champ_id'})
    table_champ_stats_up = transform.rename_cols(table_champ_stats_up, rename={'key':'champ_id'})
    
    return table_champion, table_champion_version, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats, table_champ_stats_up, table_runes

table_champion, table_champion_version, table_champ_passive, table_champ_info, table_champ_spells, table_champ_stats, table_champ_stats_up, table_runes = pipeline_champion()