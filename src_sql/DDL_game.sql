-- Schéma de la table player_id_map

CREATE TABLE player_id_map (
    player_id  SERIAL PRIMARY KEY,
    puuid      VARCHAR(78) NOT NULL UNIQUE
);

-- Schéma de la table gameid_puuid

CREATE TABLE gameid_playerid (
    player_id INTEGER,
    game_id BIGINT,
    CONSTRAINT pk_gameid_playerid
        PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_info

CREATE TABLE game_info (
    game_id BIGINT,
    match_id VARCHAR,
    end_of_game_result VARCHAR,
    game_creation TIMESTAMP,
    game_duration INTEGER,
    game_end TIMESTAMP,
    game_start TIMESTAMP,
    game_mode VARCHAR,
    game_name TEXT,
    game_type TEXT,
    game_version TEXT,
    map_id INTEGER,
    queue_id INTEGER,
    platforme_id VARCHAR,
    CONSTRAINT pk_game_info
        PRIMARY KEY (game_id)
);

-- Schéma de la table game_communication

CREATE TABLE game_communication (
    player_id INTEGER,
    game_id BIGINT,
    visionScore INTEGER,
    visionScorePerMinute REAL,
    wardsPlaced INTEGER,
    wardsKilled INTEGER,
    sightWardsBoughtInGame INTEGER,
    visionWardsBoughtInGame INTEGER,
    detectorWardsPlaced INTEGER,
    allInPings INTEGER,
    assistMePings INTEGER,
    basicPings INTEGER,
    commandPings INTEGER,
    dangerPings INTEGER,
    enemyMissingPings INTEGER,
    enemyVisionPings INTEGER,
    holdPings INTEGER,
    onMyWayPings INTEGER,
    getBackPings INTEGER,
    pushPings INTEGER,
    needVisionPings INTEGER,
    retreatPings INTEGER,
    visionClearedPings INTEGER,
    stealthWardsPlaced INTEGER,
    controlWardsPlaced INTEGER,
    wardTakedowns INTEGER,
    wardTakedownsBefore20M INTEGER,
    wardsGuarded INTEGER,
    twoWardsOneSweeperCount INTEGER,
    visionScoreAdvantageLaneOpponent REAL,
	CONSTRAINT pk_game_communication
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_capacites

CREATE TABLE game_capacites (
    player_id INTEGER,
    game_id BIGINT,
    timeCCingOthers INTEGER,
    totalTimeCCDealt INTEGER,
    spell1Casts INTEGER,
    spell2Casts INTEGER,
    spell3Casts INTEGER,
    spell4Casts INTEGER,
    summoner1Casts INTEGER,
    summoner1Id INTEGER,
    summoner2Casts INTEGER,
    summoner2Id INTEGER,
    enemyChampionImmobilizations INTEGER,
    abilityUses INTEGER,
    skillshotsHit INTEGER,
    skillshotsDodged INTEGER,
    dodgeSkillShotsSmallWindow INTEGER,
    landSkillShotsEarlyGame INTEGER,
	CONSTRAINT pk_game_capacites
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_damage

CREATE TABLE game_damage (
    player_id INTEGER,
    game_id BIGINT,
    totalDamageDealt INTEGER,
    totalDamageDealtToChampions INTEGER,
    physicalDamageDealt INTEGER,
    physicalDamageDealtToChampions INTEGER,
    magicDamageDealt INTEGER,
    magicDamageDealtToChampions INTEGER,
    trueDamageDealt INTEGER,
    trueDamageDealtToChampions INTEGER,
    damageSelfMitigated INTEGER,
    totalDamageTaken INTEGER,
    physicalDamageTaken INTEGER,
    magicDamageTaken INTEGER,
    trueDamageTaken INTEGER,
    largestCriticalStrike INTEGER,
    damagePerMinute REAL,
    teamDamagePercentage REAL,
    damageTakenOnTeamPercentage REAL,
    totalHeal INTEGER,
    totalHealsOnTeammates INTEGER,
    totalDamageShieldedOnTeammates INTEGER,
    totalUnitsHealed INTEGER,
    effectiveHealAndShielding REAL,
    saveAllyFromDeath INTEGER,
    killsOnRecentlyHealedByAramPack INTEGER,
    quickCleanse INTEGER,
	CONSTRAINT pk_game_damage
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_economie

CREATE TABLE game_economie (
    player_id INTEGER,
    game_id BIGINT,
    goldEarned INTEGER,
    goldSpent INTEGER,
    itemsPurchased INTEGER,
    consumablesPurchased INTEGER,
    item0 INTEGER,
    item1 INTEGER,
    item2 INTEGER,
    item3 INTEGER,
    item4 INTEGER,
    item5 INTEGER,
    item6 INTEGER,
    goldPerMinute REAL,
	CONSTRAINT pk_game_economie
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de table game_farming

CREATE TABLE game_farming (
    player_id INTEGER,
    game_id BIGINT,
    neutralMinionsKilled INTEGER,
    totalMinionsKilled INTEGER,
    totalAllyJungleMinionsKilled INTEGER,
    totalEnemyJungleMinionsKilled INTEGER,
    alliedJungleMonsterKills INTEGER,
    enemyJungleMonsterKills INTEGER,
    jungleCsBefore10Minutes REAL,
    scuttleCrabKills INTEGER,
    initialBuffCount INTEGER,
    initialCrabCount INTEGER,
    junglerKillsEarlyJungle REAL,
    voidMonsterKill INTEGER,
    laneMinionsFirst10Minutes INTEGER,
    moreEnemyJungleThanOpponent REAL,
    epicMonsterKillsNearEnemyJungler INTEGER,
    epicMonsterKillsWithin30SecondsOfSpawn INTEGER,
    junglerTakedownsNearDamagedEpicMonster INTEGER,
    buffsStolen INTEGER,
    maxCsAdvantageOnLaneOpponent REAL,
    maxLevelLeadLaneOpponent INTEGER,
    laningPhaseGoldExpAdvantage INTEGER,
    earlyLaningPhaseGoldExpAdvantage INTEGER,
    blastConeOppositeOpponentCount INTEGER,
    fistBumpParticipation INTEGER,
	CONSTRAINT pk_game_farming
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_fight

CREATE TABLE game_fight (
    player_id INTEGER,
    game_id BIGINT,
    kills INTEGER,
    deaths INTEGER,
    assists INTEGER,
    kda REAL,
    doubleKills INTEGER,
    tripleKills INTEGER,
    quadraKills INTEGER,
    pentaKills INTEGER,
    largestMultiKill INTEGER,
    largestKillingSpree INTEGER,
    killingSprees INTEGER,
    firstBloodKill BOOLEAN,
    firstBloodAssist BOOLEAN,
    killParticipation REAL,
    soloKills INTEGER,
    outnumberedKills INTEGER,
    killAfterHiddenWithAlly INTEGER,
    killsNearEnemyTurret INTEGER,
    killsUnderOwnTurret INTEGER,
    quickSoloKills INTEGER,
    killedChampTookFullTeamDamageSurvived INTEGER,
    killsOnLanersEarlyJungleAsJungler REAL,
    multikills INTEGER,
    multikillsAfterAggressiveFlash INTEGER,
    multiKillOneSpell INTEGER,
    legendaryCount INTEGER,
    deathsByEnemyChamps INTEGER,
    bountyGold REAL,
    maxKillDeficit INTEGER,
    takedowns INTEGER,
    takedownsFirstXMinutes INTEGER,
    takedownsAfterGainingLevelAdvantage INTEGER,
    takedownsBeforeJungleMinionSpawn INTEGER,
    takedownOnFirstTurret INTEGER,
    pickKillWithAlly INTEGER,
    immobilizeAndKillWithAlly INTEGER,
    knockEnemyIntoTeamAndKill INTEGER,
	CONSTRAINT pk_fight
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_player

CREATE TABLE game_player (
    player_id INTEGER,
    game_id BIGINT,
    riotIdGameName VARCHAR,
    riotIdTagline VARCHAR,
    summonerId VARCHAR,
    summonerLevel INTEGER,
    championId INTEGER,
    championName VARCHAR,
    champLevel INTEGER,
    champExperience INTEGER,
    participantId INTEGER,
    teamId INTEGER,
    lane VARCHAR,
    individualPosition VARCHAR,
    teamPosition VARCHAR,
    role VARCHAR,
    playedChampSelectPosition INTEGER,
    championBan INTEGER,
	CONSTRAINT pk_identite_joueur
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_objectives

CREATE TABLE game_objectives (
    player_id INTEGER,
    game_id BIGINT,
    baronKills INTEGER,
    dragonKills INTEGER,
    inhibitorKills INTEGER,
    turretKills INTEGER,
    nexusKills INTEGER,
    objectivesStolen INTEGER,
    objectivesStolenAssists INTEGER,
    damageDealtToObjectives INTEGER,
    damageDealtToBuildings INTEGER,
    damageDealtToEpicMonsters INTEGER,
    damageDealtToTurrets INTEGER,
    firstTowerKill BOOLEAN,
    firstTowerAssist BOOLEAN,
    turretTakedowns INTEGER,
    nexusTakedowns INTEGER,
    inhibitorTakedowns INTEGER,
    turretPlatesTaken INTEGER,
    baronTakedowns INTEGER,
    riftHeraldTakedowns INTEGER,
    dragonTakedowns INTEGER,
    epicMonsterSteals INTEGER,
    epicMonsterStolenWithoutSmite INTEGER,
    teamBaronKills INTEGER,
    teamElderDragonKills INTEGER,
    teamRiftHeraldKills INTEGER,
    soloBaronKills INTEGER,
    elderDragonKillsWithOpposingSoul INTEGER,
    elderDragonMultikills INTEGER,
    perfectDragonSoulsTaken INTEGER,
    kTurretsDestroyedBeforePlatesFall INTEGER,
    outerTurretExecutesBefore10Minutes INTEGER,
    quickFirstTurret INTEGER,
    multiTurretRiftHeraldCount INTEGER,
    turretsTakenWithRiftHerald INTEGER,
    takedownsInAlcove INTEGER,
    takedownsInEnemyFountain INTEGER,
    outnumberedNexusKill INTEGER,
    hadOpenNexus INTEGER,
    dancedWithRiftHerald INTEGER,
    killsWithHelpFromEpicMonster INTEGER,
	CONSTRAINT pk_objective_structures
		PRIMARY KEY (player_id, game_id)
);

-- Schéma de la table game_performance

CREATE TABLE game_performance (
    player_id INTEGER,
    game_id BIGINT,
    win BOOLEAN,
    timePlayed INTEGER,
    longestTimeSpentLiving INTEGER,
    totalTimeSpentDead INTEGER,
    gameEndedInSurrender BOOLEAN,
    gameEndedInEarlySurrender BOOLEAN,
    teamEarlySurrendered BOOLEAN,
    inhibitorsLost INTEGER,
    nexusLost INTEGER,
    turretsLost INTEGER,
    eligibleForProgression BOOLEAN,
    lostAnInhibitor INTEGER,
    flawlessAces INTEGER,
    doubleAces INTEGER,
    acesBefore15Minutes INTEGER,
    fullTeamTakedown INTEGER,
    perfectGame INTEGER,
	CONSTRAINT pk_perf_globale
		PRIMARY KEY (player_id, game_id)
);