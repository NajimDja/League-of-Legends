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