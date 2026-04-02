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