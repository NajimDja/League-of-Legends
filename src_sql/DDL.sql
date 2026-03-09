-- Schéma de la table champion

CREATE TABLE champion (
    id      INTEGER,
    name    TEXT,
    title   TEXT,
    lore    TEXT,
    tags    TEXT,
    partype TEXT,
    version TEXT,
    CONSTRAINT pk_champion
        PRIMARY KEY (id)
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
    range_burn   INTEGER,
    spell_rank   INTEGER,
    version      TEXT,
    CONSTRAINT pk_champion_spells
        PRIMARY KEY (spell_id, champ_id, version),
    CONSTRAINT fk_champion_spells_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE
);