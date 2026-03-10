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

