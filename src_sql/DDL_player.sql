-- Schéma de la table account

CREATE TABLE account (
    puuid VARCHAR(78),
    player_id INTEGER,
    game_name VARCHAR,
    tag_line VARCHAR,
    CONSTRAINT pk_account
        PRIMARY KEY (player_id)
);

-- Schéma de la table summoner

CREATE TABLE summoner (
    player_id INTEGER,
    profil_icon_id INTEGER,
    last_modif TIMESTAMP,
    summoner_level INTEGER,
    CONSTRAINT pk_summoner
        PRIMARY KEY (player_id),
    CONSTRAINT fk_summoner_account
        FOREIGN KEY (player_id) REFERENCES account(player_id)
        ON DELETE CASCADE
);

-- Schéma de la table champion_mastery

CREATE TABLE champion_mastery (
    player_id INTEGER,
    champ_id INTEGER,
    champ_level INTEGER,
    champ_points INTEGER,
    last_time_played TIMESTAMP,
    points_to_next_level INTEGER,
    CONSTRAINT pk_champion_mastery
        PRIMARY KEY (player_id, champ_id),
    CONSTRAINT fk_champion_mastery_account
        FOREIGN KEY (player_id) REFERENCES account(player_id)
        ON DELETE CASCADE
);

-- Schéma de la table challenges

CREATE TABLE challenges (
    player_id INTEGER,
    challenge_id INTEGER,
    percentile REAL,
    level VARCHAR,
    level_index	INTEGER,
    value INTEGER,
    achieved_time TIMESTAMP,
    description	TEXT,
    name	TEXT,
    CONSTRAINT pk_challenges
        PRIMARY KEY (player_id, challenge_id),
    CONSTRAINT fk_challenges_account
        FOREIGN KEY (player_id) REFERENCES account(player_id)
        ON DELETE CASCADE
);

-- Schéma de la table queue

CREATE TABLE queue (
    player_id INTEGER,
    league_id VARCHAR,
    queue_type	VARCHAR,
    tier	VARCHAR,
    rank	VARCHAR,
    league_points	INTEGER,
    wins	INTEGER,
    losses INTEGER,
    CONSTRAINT pk_queue
        PRIMARY KEY (player_id, league_id),
    CONSTRAINT fk_queue_account
        FOREIGN KEY (player_id) REFERENCES account(player_id)
        ON DELETE CASCADE
);