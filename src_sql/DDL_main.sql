-------------------------------
-- TABLES PLAYERS
-------------------------------

-- Schéma de la table account

CREATE TABLE account (
    puuid VARCHAR(78),
    game_name VARCHAR,
    tagline VARCHAR,
    CONSTRAINT pk_account
        PRIMARY KEY (puuid)
);

-- Schéma de la table summoner

CREATE TABLE summoner (
    puuid VARCHAR(78),
    profil_icon_id INTEGER,
    revision_date TIMESTAMP,
    summoner_level INTEGER,
    CONSTRAINT pk_summoner
        PRIMARY KEY (puuid),
    CONSTRAINT fk_summoner_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);

-- Schéma de la table champion_mastery

CREATE TABLE champion_mastery (
    puuid VARCHAR(78),
    champ_id INTEGER,
    champ_level INTEGER,
    champ_points INTEGER,
    last_time_played TIMESTAMP,
    points_to_next_level INTEGER,
    CONSTRAINT pk_champion_mastery
        PRIMARY KEY (puuid, champ_id),
    CONSTRAINT fk_champion_mastery_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);


-------------------------------
-- TABLES GAMES
-------------------------------

-- Schéma de la table game

CREATE TABLE game (
    game_id VARCHAR,
    puuid VARCHAR(78),
    champ_id INTEGER,
    champ_name VARCHAR,
    lane VARCHAR,
    win BOOLEAN,
    CONSTRAINT pk_game
        PRIMARY KEY (game_id, puuid),
    CONSTRAINT fk_game_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);

-- Schéma de la table game_info

CREATE TABLE game_info (
    game_id VARCHAR,
    end_game_result VARCHAR,
    game_creation TIMESTAMP,
    game_duration VARCHAR,
    game_end TIMESTAMP,
    game_start TIMESTAMP,
    game_mode VARCHAR,
    game_name TEXT,
    game_type TEXT,
    game_version TEXT,
    map_id,
    CONSTRAINT pk_game_info
        PRIMARY KEY (game_id)
);

-- Schéma de la table game_item (table d'association item_id, game_id, puuid)

CREATE TABLE game_item (
    game_id VARCHAR,
    puuid   VARCHAR(78),
    item_id INTEGER,
    CONSTRAINT pk_game_item
        PRIMARY KEY (game_id, puuid, item_id),
    CONSTRAINT fk_game_item_game
        FOREIGN KEY (game_id, puuid) REFERENCES game(game_id, puuid)
        ON DELETE CASCADE
);

-- Schéma de la table items

CREATE TABLE items (
    item_id INTEGER,
    name TEXT,
    description TEXT,
    cost NUMERIC,
    sell NUMERIC,
    stats TEXT,
    CONSTRAINT pk_item
        PRIMARY KEY (item_id)
);

-- Schéma de la table ranked

CREATE TABLE ranked (
    puuid VARCHAR(78),
    league_id TEXT,
    queue_type TEXT,
    tier VARCHAR,
    rank VARCHAR,
    league_points INTEGER,
    wins INTEGER,
    losses INTEGER,
    veteran BOOLEAN,
    inactive BOOLEAN,
    fresh_blood BOOLEAN,
    hot_streak BOOLEAN,
    CONSTRAINT pk_ranked
        PRIMARY KEY (puuid, league_id),
    CONSTRAINT fk_ranked_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);


-------------------------------
-- TABLES CHAMPIONS
-------------------------------

-- Schéma de la table champion

CREATE TABLE champion (
    id      INTEGER,
    name    TEXT NOT NULL,
    title   TEXT,
    lore    TEXT,
    tags    TEXT,
    partype TEXT,
    version TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE
    CONSTRAINT pk_champion
        PRIMARY KEY (id)
);

-- Schéma de la table champion_info

CREATE TABLE champion_info (
    champ_id INTEGER,
    allytips TEXT,
    enemytips TEXT,
    attack	INTEGER,
    defense	INTEGER,
    magic	INTEGER,
    difficulty INTEGER,
    version TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_champion_info
        PRIMARY KEY (champ_id, version),
    CONSTRAINT fk_champion_info_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);

-- schéma de la table champion_passive

CREATE TABLE champion_passive (
    champ_id INTEGER,
    name	TEXT,
    description	TEXT,
    version TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_champion_passive
        PRIMARY KEY (champ_id, version),
    CONSTRAINT fk_champion_passive_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);

-- Schéma de la table champion_spells

CREATE TABLE champion_spells (
    champ_id     INTEGER,
    spell_id     TEXT,
    spell_name   TEXT,
    tooltip      TEXT,
    maxrank      INTEGER,
    cooldown_burn TEXT,
    cost_burn    TEXT,
    cost_type    TEXT,
    maxammo      INTEGER,
    range_burn   VARCHAR,
    spell_rank   INTEGER,
    version      TEXT,
    is_latest    BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_champion_spells
        PRIMARY KEY (spell_id, champ_id, version),
    CONSTRAINT fk_champion_spells_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);

-- Schéma de la table champion_stats

CREATE TABLE champion_stats (
    champ_id INTEGER,
    hp	INTEGER,
    mp	INTEGER,
    movespeed	INTEGER,
    armor	INTEGER,
    spellblock	INTEGER,
    attackrange	INTEGER,
    hpregen	REAL,
    mpregen	REAL,
    crit	INTEGER,
    attackdamage	INTEGER,
    attackspeed	REAL,
    version TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_champion_stats
        PRIMARY KEY (champ_id, version),
    CONSTRAINT fk_champion_stats_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);

-- Schéma de la table champion_stats_up

CREATE TABLE champion_stats_up (
    champ_id INTEGER,
    hp_up	INTEGER,
    mp_up	REAL,
    armor_up	REAL,
    spellblock_up REAL,
    hpregen_up	REAL,
    mpregen_up	REAL,
    crit_up	REAL,
    attackdamage_up	REAL,
    attackspeed_up	REAL,
    version TEXT,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_champion_stats_up
        PRIMARY KEY (champ_id, version),
    CONSTRAINT fk_champion_stats_up_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);