----------------
-- View tables
----------------

SELECT * FROM patch;
SELECT COUNT(0) FROM patch;

SELECT * FROM champion;
SELECT COUNT(0) FROM champion;

SELECT * FROM champion_version;

SELECT * FROM champion_passive;

SELECT * FROM champion_info;

SELECT * FROM champion_spells;

SELECT * FROM champion_stats;

SELECT * FROM champion_stats_up;

----------------------
-- View joins
----------------------

SELECT s.hp, u.hp_up
FROM champion_stats s
INNER JOIN champion_stats_up u ON s.champ_id = u.champ_id;
-- ou
SELECT s.hp, u.hp_up
FROM champion_stats s
INNER JOIN champion_stats_up u USING (champ_id);

SELECT a.hp, a.hp_up, a."HP max", a."AD max", a."MP max", c.name
FROM (
    SELECT s.champ_id, s.hp, u.hp_up, 
    (s.hp + u.hp_up * 18) AS "HP max",
    (s.attackdamage + u.attackdamage_up * 18) AS "AD max",
    (s.mp + u.mp_up * 18) AS "MP max"
    FROM champion_stats s
    INNER JOIN champion_stats_up u USING (champ_id)
    ) a
INNER JOIN champion c ON c.id = a.champ_id
ORDER BY c.name;
