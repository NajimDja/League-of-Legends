------------------------------
-- Statistiques des joueurs --
------------------------------

-- Nombre de game, win_rate et temps de jeu par joueur
SELECT 
    a.game_name AS "Pseudo",
    COUNT(*) AS total_games,
    ROUND(
        AVG(CASE WHEN gpr.win THEN 1.0 ELSE 0 END)*100,2)::text || '%' AS win_rate,
    TO_CHAR(
        (SUM(timeplayed) || ' seconds')::interval,
        'HH24:MI:SS'
    ) AS temps_de_jeu
FROM game_performance gpr
JOIN account a ON gpr.player_id = a.player_id
GROUP BY a.player_id, a.game_name
ORDER BY total_games DESC;


-- Nombre de game, win_rate et temps de jeu par joueur et poste
SELECT 
    a.game_name AS pseudo,
    gpi.individualposition AS lane,
    COUNT(*) AS total_games,
    ROUND(
        AVG(CASE WHEN gpr.win THEN 1.0 ELSE 0 END)*100,
        2)::text || '%' AS win_rate,
    TO_CHAR(
        (SUM(timeplayed) || ' seconds')::interval,
        'HH24:MI:SS'
    ) AS temps_de_jeu
FROM game_performance gpr
JOIN account a 
    ON gpr.player_id = a.player_id
JOIN game_player_info gpi 
    ON gpr.player_id = gpi.player_id
    AND gpr.game_id = gpi.game_id
WHERE gpi.individualposition != 'Invalid'
GROUP BY a.player_id, a.game_name, gpi.individualposition
ORDER BY pseudo, total_games DESC;


-- Nombre de game, win_rate et temps de jeu par joueur et champion
SELECT 
    a.game_name AS pseudo,
    gpi.championname AS nom_champion,
    COUNT(*) AS total_games,
    ROUND(
        AVG(CASE WHEN gpr.win THEN 1.0 ELSE 0 END)*100,
        2)::text || '%' AS win_rate,
    TO_CHAR(
        (SUM(timeplayed) || ' seconds')::interval,
        'HH24:MI:SS'
    ) AS temps_de_jeu
FROM game_performance gpr
JOIN account a 
    ON gpr.player_id = a.player_id
JOIN game_player_info gpi 
    ON gpr.player_id = gpi.player_id
    AND gpr.game_id = gpi.game_id
GROUP BY a.player_id, a.game_name, gpi.championname
ORDER BY pseudo, total_games DESC;


-- Nombre de game par joueur et queue
SELECT
    a.game_name AS pseudo,
    gi.queue_id AS queue,
    CASE gi.queue_id
        WHEN 400 THEN '5v5 Draft Pick games' 
        WHEN 420 THEN '5v5 Ranked Solo games'
        WHEN 440 THEN '5v5 Ranked Flex games'
        WHEN 480 THEN 'Swiftplay Games'
        WHEN 490 THEN 'Normal (Quickplay)'
    END AS type_game,
    COUNT(0) AS total_games
FROM game_player gp
JOIN account a
    ON gp.player_id = a.player_id
JOIN game_info gi
    ON gp.game_id = gi.game_id
GROUP BY pseudo, queue
ORDER BY pseudo, queue;

--------------------------------
-- Statistiques des game info --
--------------------------------

-- Durée moyenne d'une game, mode le plus joué
SELECT
    TO_CHAR(
        (AVG(gi.game_duration) || ' seconds')::interval,
        'HH24:MI:SS'
    ) AS temps_moyen_game,
    mode() WITHIN GROUP (ORDER BY queue_id) AS most_mode_played,
    mode() WITHIN GROUP (ORDER BY end_of_game_result) AS most_type_end
FROM game_info gi;

-- Champion les plus joués, winrate
SELECT
    gpi.individualposition AS lane,
    gpi.championname AS champion,
    COUNT(0) AS nb_game,
    ROUND(
        AVG(CASE WHEN gpr.win THEN 1.0 ELSE 0 END)*100,
        2)::text || '%' AS win_rate
FROM game_player_info gpi
INNER JOIN game_performance gpr 
    ON gpi.game_id = gpr.game_id
    AND gpi.player_id = gpr.player_id
GROUP BY lane, champion
ORDER BY nb_game DESC;

-- Champion les plus joués, winrate, nb_game par lane et champion
SELECT
    gpi.individualposition AS lane,
    gpi.championname AS champion,
    COUNT(0) AS nb_game,
    ROUND(
        AVG(CASE WHEN gpr.win THEN 1.0 ELSE 0 END)*100,
        2) AS win_rate
FROM game_player_info gpi
INNER JOIN game_performance gpr
    ON gpi.game_id = gpr.game_id
    AND gpi.player_id = gpr.player_id
WHERE gpi.individualposition NOT IN ('Invalid', 'Unknown', '')
GROUP BY gpi.individualposition, champion
HAVING COUNT(0) > 20
ORDER BY lane, win_rate DESC;

-- Champion les plus ban
SELECT
    c.name AS champion_ban,
    COUNT(0) AS nb_ban
FROM game_player_info gpi
INNER JOIN champion c
    ON gpi.championban = c.id
WHERE gpi.championban IS NOT NULL
GROUP BY c.name
ORDER BY nb_ban DESC;