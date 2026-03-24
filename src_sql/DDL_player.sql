-- Schéma de la table account

CREATE TABLE account (
    puuid VARCHAR(78),
    game_name VARCHAR,
    tag_line VARCHAR,
    CONSTRAINT pk_account
        PRIMARY KEY (puuid)
);

-- Schéma de la table summoner

CREATE TABLE summoner (
    puuid VARCHAR(78),
    profil_icon_id INTEGER,
    last_modif TIMESTAMP,
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

-- Schéma de la table challenges

CREATE TABLE challenges (
    puuid VARCHAR(78),
    challenge_id INTEGER,
    percentile REAL,
    level VARCHAR,
    level_index	INTEGER,
    value INTEGER,
    achieved_time TIMESTAMP,
    description	TEXT,
    name	TEXT,
    CONSTRAINT pk_challenges
        PRIMARY KEY (puuid, challenge_id),
    CONSTRAINT fk_challenges_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);

-- Schéma de la table queue

CREATE TABLE queue (
    puuid VARCHAR(78),
    league_id VARCHAR,
    queue_type	VARCHAR,
    tier	VARCHAR,
    rank	VARCHAR,
    league_points	INTEGER,
    wins	INTEGER,
    losses INTEGER,
    CONSTRAINT pk_queue
        PRIMARY KEY (puuid, league_id),
    CONSTRAINT fk_queue_account
        FOREIGN KEY (puuid) REFERENCES account(puuid)
        ON DELETE CASCADE
);