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
                    "mejaisFullStackInTime", "tookLargeDamageSurvived",
                    "twentyMinionsIn3SecondsCount", "unseenRecalls", "killingSprees", "turretTakedowns"
                    ]
    
    identite_joueur = ["puuid", "game_id",
        "riotIdGameName", "riotIdTagline", "summonerId",
        "summonerLevel", "championId", "championName",
        "champLevel", "champExperience", "participantId", "teamId",
        "lane", "individualPosition", "teamPosition", "role",
        "playedChampSelectPosition"
    ]

    combat = ["puuid", "game_id",
            "kills", "deaths", "assists", "kda", "doubleKills", "tripleKills", "quadraKills", "pentaKills",
            "largestMultiKill", "largestKillingSpree", "killingSprees", "firstBloodKill", "firstBloodAssist", 
            "killParticipation", "soloKills", "outnumberedKills", "killAfterHiddenWithAlly", "killsNearEnemyTurret", 
            "killsUnderOwnTurret", "quickSoloKills", "killedChampTookFullTeamDamageSurvived",
            "killsOnLanersEarlyJungleAsJungler", "multikills", "multikillsAfterAggressiveFlash", "multiKillOneSpell",
            "legendaryCount", "deathsByEnemyChamps", "bountyGold",
            "maxKillDeficit", "takedowns", "takedownsFirstXMinutes", "takedownsAfterGainingLevelAdvantage",
            "takedownsBeforeJungleMinionSpawn", "takedownOnFirstTurret", "pickKillWithAlly", "immobilizeAndKillWithAlly",
            "knockEnemyIntoTeamAndKill"
    ]

    degats = ["puuid", "game_id",
        "totalDamageDealt", "totalDamageDealtToChampions",
        "physicalDamageDealt", "magicDamageDealt", "trueDamageDealt",
        "physicalDamageDealtToChampions", "magicDamageDealtToChampions",
        "trueDamageDealtToChampions", "damageSelfMitigated",
        "totalDamageTaken", "physicalDamageTaken", "magicDamageTaken", "trueDamageTaken",
        "largestCriticalStrike",
        "damagePerMinute", "teamDamagePercentage",
        "damageTakenOnTeamPercentage"
    ]

    jungle_farm = ["puuid", "game_id",
        "neutralMinionsKilled", "totalMinionsKilled",
        "totalAllyJungleMinionsKilled", "totalEnemyJungleMinionsKilled",
        "alliedJungleMonsterKills", "enemyJungleMonsterKills",
        "jungleCsBefore10Minutes", "scuttleCrabKills",
        "initialBuffCount", "initialCrabCount",
        "junglerKillsEarlyJungle", "voidMonsterKill",
        "laneMinionsFirst10Minutes", "moreEnemyJungleThanOpponent",
        "epicMonsterKillsNearEnemyJungler",
        "epicMonsterKillsWithin30SecondsOfSpawn",
        "junglerTakedownsNearDamagedEpicMonster",
        "buffsStolen"
    ]
    
    objectifs_structures = ["puuid", "game_id",
        "baronKills", "dragonKills", "inhibitorKills",
        "turretKills", "nexusKills", "objectivesStolen", "objectivesStolenAssists",
        "damageDealtToObjectives", "damageDealtToBuildings",
        "damageDealtToEpicMonsters", "damageDealtToTurrets",
        "firstTowerKill", "firstTowerAssist",
        "turretTakedowns", "nexusTakedowns", "inhibitorTakedowns",
        "turretPlatesTaken", "baronTakedowns",
        "riftHeraldTakedowns", "dragonTakedowns",
        "epicMonsterSteals", "epicMonsterStolenWithoutSmite",
        "teamBaronKills", "teamElderDragonKills",
        "teamRiftHeraldKills", "soloBaronKills",
        "elderDragonKillsWithOpposingSoul", "elderDragonMultikills",
        "perfectDragonSoulsTaken",
        "kTurretsDestroyedBeforePlatesFall",
        "outerTurretExecutesBefore10Minutes",
        "quickFirstTurret", "multiTurretRiftHeraldCount",
        "turretsTakenWithRiftHerald", "takedownsInAlcove",
        "takedownsInEnemyFountain", "outnumberedNexusKill",
        "hadOpenNexus", "dancedWithRiftHerald",
        "killsWithHelpFromEpicMonster"
    ] #earliestBaron
    
    vision_communication = ["puuid", "game_id",
        "visionScore", "wardsPlaced", "wardsKilled",
        "sightWardsBoughtInGame", "visionWardsBoughtInGame", "detectorWardsPlaced",
        "allInPings", "assistMePings", "basicPings", "commandPings", "dangerPings",
        "enemyMissingPings", "enemyVisionPings", "holdPings", "onMyWayPings",
        "getBackPings", "pushPings", "needVisionPings", "retreatPings", "visionClearedPings",
        "stealthWardsPlaced", "controlWardsPlaced",
        "visionScorePerMinute", "wardTakedowns",
        "wardTakedownsBefore20M", "wardsGuarded",
        "twoWardsOneSweeperCount", "visionScoreAdvantageLaneOpponent"
    ]

    economie_items = ["puuid", "game_id",
        "goldEarned", "goldSpent", "itemsPurchased", "consumablesPurchased",
        "item0", "item1", "item2", "item3", "item4", "item5", "item6",
        "goldPerMinute"
    ]

    soins_soutien = ["puuid", "game_id",
        "totalHeal", "totalHealsOnTeammates",
        "totalDamageShieldedOnTeammates", "totalUnitsHealed",
        "effectiveHealAndShielding", "saveAllyFromDeath", 
        "killsOnRecentlyHealedByAramPack",
        "quickCleanse"
    ]

    cc_capacites = ["puuid", "game_id",
        "timeCCingOthers", "totalTimeCCDealt",
        "spell1Casts", "spell2Casts", "spell3Casts", "spell4Casts",
        "summoner1Casts", "summoner1Id", "summoner2Casts", "summoner2Id",
        "enemyChampionImmobilizations", "abilityUses",
        "skillshotsHit", "skillshotsDodged",
        "dodgeSkillShotsSmallWindow", "landSkillShotsEarlyGame"
    ]

    phase_de_lane = ["puuid", "game_id",
        "maxCsAdvantageOnLaneOpponent", "maxLevelLeadLaneOpponent",
        "laningPhaseGoldExpAdvantage", "earlyLaningPhaseGoldExpAdvantage",
        "blastConeOppositeOpponentCount", "fistBumpParticipation"
    ]

    performance_globale = ["puuid", "game_id",
        "win", "timePlayed", "longestTimeSpentLiving", "totalTimeSpentDead",
        "gameEndedInSurrender", "gameEndedInEarlySurrender", "teamEarlySurrendered",
        "inhibitorsLost", "nexusLost", "turretsLost", "eligibleForProgression",
        "lostAnInhibitor", "flawlessAces", "doubleAces",
        "acesBefore15Minutes", "fullTeamTakedown", "perfectGame"
    ]