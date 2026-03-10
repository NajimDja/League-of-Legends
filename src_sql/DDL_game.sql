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