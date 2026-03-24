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

-- Schéma de la table items

CREATE TABLE items (
    item_id INTEGER,
    patch_id INTEGER,
    name TEXT,
    description TEXT,
    stats TEXT,
    cost INTEGER,
    sell INTEGER,
    tags TEXT,
    CONSTRAINT pk_item
        PRIMARY KEY (item_id)
);

-- Schéma de la table runes

CREATE TABLE runes (
    type_rune_id	INTEGER,
    type_name	TEXT,
    child_rune_id	INTEGER,
    name	TEXT,
    description	TEXT,
    patch_id INTEGER,
    CONSTRAINT pk_runes
        PRIMARY KEY (type_rune_id, child_rune_id)
);