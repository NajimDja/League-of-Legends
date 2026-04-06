-- Schéma de la table game_info

CREATE TABLE game_info (
    game_id INTEGER,
    match_id VARCHAR,
    end_of_game_result VARCHAR,
    game_creation TIMESTAMP,
    game_duration VARCHAR,
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

-- Schéma de la table communication

CREATE TABLE communication (
    puuid VARCHAR,
    game_id INTEGER,
    visionScore INTEGER,
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
    visionScorePerMinute REAL,
    wardTakedowns INTEGER,
    wardTakedownsBefore20M INTEGER,
    wardsGuarded INTEGER,
    twoWardsOneSweeperCount INTEGER,
    visionScoreAdvantageLaneOpponent REAL,
	CONSTRAINT pk_communication
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE cc_capacites (
    puuid VARCHAR,
    game_id INTEGER,
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
	CONSTRAINT pk_cc_capacites
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE damage (
    puuid VARCHAR,
    game_id INTEGER,
    totalDamageDealt INTEGER,
    totalDamageDealtToChampions INTEGER,
    physicalDamageDealt INTEGER,
    magicDamageDealt INTEGER,
    trueDamageDealt INTEGER,
    physicalDamageDealtToChampions INTEGER,
    magicDamageDealtToChampions INTEGER,
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
	CONSTRAINT pk_damage
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE economie_items (
    puuid VARCHAR,
    game_id INTEGER,
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
	CONSTRAINT pk_economie_items
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE farming (
    puuid VARCHAR,
    game_id INTEGER,
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
	CONSTRAINT pk_farming
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE fight (
    puuid VARCHAR,
    game_id INTEGER,
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
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE identite_joueur (
    puuid VARCHAR,
    game_id INTEGER,
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
	CONSTRAINT pk_identite_joueur
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE objective_structures (
    puuid VARCHAR,
    game_id INTEGER,
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
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE perf_globale (
    puuid VARCHAR,
    game_id INTEGER,
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
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE phase_de_lane (
    puuid VARCHAR,
    game_id INTEGER,
    maxCsAdvantageOnLaneOpponent REAL,
    maxLevelLeadLaneOpponent INTEGER,
    laningPhaseGoldExpAdvantage INTEGER,
    earlyLaningPhaseGoldExpAdvantage INTEGER,
    blastConeOppositeOpponentCount INTEGER,
    fistBumpParticipation INTEGER,
	CONSTRAINT pk_phase_de_lane
		PRIMARY KEY (puuid, game_id)
);

CREATE TABLE soins_soutien (
    puuid VARCHAR,
    game_id INTEGER,
    totalHeal INTEGER,
    totalHealsOnTeammates INTEGER,
    totalDamageShieldedOnTeammates INTEGER,
    totalUnitsHealed INTEGER,
    effectiveHealAndShielding REAL,
    saveAllyFromDeath INTEGER,
    killsOnRecentlyHealedByAramPack INTEGER,
    quickCleanse INTEGER,
	CONSTRAINT pk_soins_soutien
		PRIMARY KEY (puuid, game_id)
);