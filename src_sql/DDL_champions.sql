-------------------------------
-- TABLE PATCH
-------------------------------

CREATE TABLE patch (
    id        INTEGER,
    version   TEXT NOT NULL UNIQUE,
    is_latest BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT pk_patch
        PRIMARY KEY (id)
);

-------------------------------
-- TABLES CHAMPIONS
-------------------------------

CREATE TABLE champion (
    id   INTEGER,
    name TEXT NOT NULL,
    CONSTRAINT pk_champion
        PRIMARY KEY (id)
);

CREATE TABLE champion_version (
    champ_id INTEGER NOT NULL,
    patch_id INTEGER NOT NULL,
    title    TEXT,
    lore     TEXT,
    tags     TEXT,
    partype  TEXT,
    CONSTRAINT pk_champion_version
        PRIMARY KEY (champ_id, patch_id),
    CONSTRAINT fk_champion_version_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_version_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);

CREATE TABLE champion_info (
    champ_id   INTEGER,
    patch_id   INTEGER,
    allytips   TEXT,
    enemytips  TEXT,
    attack     INTEGER,
    defense    INTEGER,
    magic      INTEGER,
    difficulty INTEGER,
    CONSTRAINT pk_champion_info
        PRIMARY KEY (champ_id, patch_id),
    CONSTRAINT fk_champion_info_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_info_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);

CREATE TABLE champion_passive (
    champ_id    INTEGER,
    patch_id    INTEGER,
    name        TEXT,
    description TEXT,
    CONSTRAINT pk_champion_passive
        PRIMARY KEY (champ_id, patch_id),
    CONSTRAINT fk_champion_passive_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_passive_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);

CREATE TABLE champion_spells (
    champ_id      INTEGER,
    spell_id      TEXT,
    patch_id      INTEGER,
    spell_name    TEXT,
    tooltip       TEXT,
    maxrank       INTEGER,
    cooldown_burn TEXT,
    cost_burn     TEXT,
    cost_type     TEXT,
    maxammo       INTEGER,
    range_burn    VARCHAR,
    spell_rank    INTEGER,
    CONSTRAINT pk_champion_spells
        PRIMARY KEY (spell_id, champ_id, patch_id),
    CONSTRAINT fk_champion_spells_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_spells_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);

CREATE TABLE champion_stats (
    champ_id    INTEGER,
    patch_id    INTEGER,
    hp          INTEGER,
    mp          INTEGER,
    movespeed   INTEGER,
    armor       INTEGER,
    spellblock  INTEGER,
    attackrange INTEGER,
    hpregen     REAL,
    mpregen     REAL,
    crit        INTEGER,
    attackdamage INTEGER,
    attackspeed REAL,
    CONSTRAINT pk_champion_stats
        PRIMARY KEY (champ_id, patch_id),
    CONSTRAINT fk_champion_stats_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_stats_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);

CREATE TABLE champion_stats_up (
    champ_id        INTEGER,
    patch_id        INTEGER,
    hp_up           INTEGER,
    mp_up           REAL,
    armor_up        REAL,
    spellblock_up   REAL,
    hpregen_up      REAL,
    mpregen_up      REAL,
    crit_up         REAL,
    attackdamage_up REAL,
    attackspeed_up  REAL,
    CONSTRAINT pk_champion_stats_up
        PRIMARY KEY (champ_id, patch_id),
    CONSTRAINT fk_champion_stats_up_champion
        FOREIGN KEY (champ_id) REFERENCES champion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_champion_stats_up_patch
        FOREIGN KEY (patch_id) REFERENCES patch(id)
        ON DELETE CASCADE
);