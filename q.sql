SELECT
    s.EVENT_WYID,
    s.MATCH_WYID,
    s.PRIMARYTYPE,
    s.SHOTBODYPART,
    s.SHOTISGOAL,
    s.SHOTONTARGET,
    s.SHOTGOALZONE,
    s.SHOTXG,
    s.SHOTPOSTSHOTXG,

    -- Shooter info
    CONCAT(sh.FIRSTNAME, ' ', sh.LASTNAME) AS shooter_name,
    sh.ROLENAME AS shooter_role,
    sh.FOOT AS shooter_foot,

    -- Goalkeeper info
    CONCAT(gk.FIRSTNAME, ' ', gk.LASTNAME) AS goalkeeper_name,

    -- Event context
    e.MATCHPERIOD,
    e.MINUTE,
    e.SECOND,
    e.LOCATIONX,
    e.LOCATIONY,
    e.TEAM_WYID,
    t.TEAMNAME AS team_name,
    ot.TEAMNAME AS opponent_name,

    -- Match info (score, side)
    m.SIDE AS team_side,
    m.SCORE AS team_score,
    m.SCOREHT AS team_score_ht

FROM wyscout_matchevents_shots s

JOIN wyscout_matchevents_common e
    ON s.EVENT_WYID = e.EVENT_WYID

LEFT JOIN wyscout_players sh
    ON e.PLAYER_WYID = sh.PLAYER_WYID
    AND sh.SEASON_WYID = e.SEASON_WYID

LEFT JOIN wyscout_players gk
    ON s.SHOTGOALKEEPER_WYID = gk.PLAYER_WYID
    AND gk.SEASON_WYID = e.SEASON_WYID

LEFT JOIN wyscout_teams t
    ON e.TEAM_WYID = t.TEAM_WYID
    AND e.SEASON_WYID = t.SEASON_WYID
    

LEFT JOIN wyscout_teams ot
    ON e.OPPONENTTEAM_WYID = ot.TEAM_WYID
    AND e.SEASON_WYID = ot.SEASON_WYID

LEFT JOIN wyscout_matchdetail_base m
    ON s.MATCH_WYID = m.MATCH_WYID
   AND e.TEAM_WYID = m.TEAM_WYID

WHERE s.PRIMARYTYPE = 'Shot';

