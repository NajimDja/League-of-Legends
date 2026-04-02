# Clés à conserver ou supprimer des données de l'api riot

class KeysData:

    keys_ids = ['puuid', 'game_id']

    keys_match_info = ["endOfGameResult", "gameCreation", "gameDuration", "gameEndTimestamp", "gameId", 
                        "gameMode", "gameName", "gameStartTimestamp", "gameType", "gameVersion", "mapId", 
                        "platformId", "queueId"]
    
    keys_to_reject = ["missions", "PlayerBehavior", "PlayerScore0", "PlayerScore1", "PlayerScore10",
                    "PlayerScore11", "PlayerScore2", "PlayerScore3", "PlayerScore4", "PlayerScore5",
                    "PlayerScore6", "PlayerScore7", "PlayerScore8", "PlayerScore9", "challenges",
                    "placement", "playerAugment1", "playerAugment2", "playerAugment3", "playerAugment4",
                    "playerAugment5", "playerAugment6", "playerSubteamId", "profileIcon", "subteamPlacement",
                    "perks"]
    
    keys_to_reject_challenges = ["12AssistStreakCount", "HealFromMapSources", "InfernalScalePickup",
                    "SWARM_DefeatAatrox", "SWARM_DefeatBriar", "SWARM_DefeatMiniBosses",
                    "SWARM_EvolveWeapon", "SWARM_Have3Passives", "SWARM_KillEnemy",
                    "SWARM_PickupGold", "SWARM_ReachLevel50", "SWARM_Survive15Min",
                    "SWARM_WinWith5EvolvedWeapons", "gameLength", "legendaryItemUsed", "poroExplosions",
                    "snowballsHit", "survivedSingleDigitHpCount", "survivedThreeImmobilizesInFight",
                    "mejaisFullStackInTime", "outerTurretExecutesBefore10Minutes", "tookLargeDamageSurvived",
                    "twentyMinionsIn3SecondsCount", "twoWardsOneSweeperCount", "unseenRecalls",
                    "dancedWithRiftHerald", "multiTurretRiftHeraldCount", "riftHeraldTakedowns",
                    "teamRiftHeraldKills", "turretsTakenWithRiftHerald"]