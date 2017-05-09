-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
  player_id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES players(player_id),
  loser INTEGER REFERENCES players(player_id)
);

CREATE VIEW count_wins AS
  /* Selects the player id, counts the number of wins by that player, and
  joins the players.player_id column with the maches.winner column */
  SELECT p.player_id, COUNT(*) AS wins
  FROM players AS p
  INNER JOIN matches AS m
    ON p.player_id = m.winner
  GROUP BY p.player_id, m.winner
  ORDER BY wins DESC;

CREATE VIEW count_losses AS
  /* Selects the player id, counts the number of losses by that player, and
  joins the players.player_id column with the maches.loser column */
  SELECT p.player_id, COUNT(*) AS losses
  FROM players AS p
  INNER JOIN matches AS m
    ON p.player_id = m.loser
  GROUP BY p.player_id, m.loser
  ORDER BY losses DESC;

CREATE VIEW match_stats AS
  /* View uses coalesce function to return non-null results from count_wins
  and count_losses and associate the win/loss ratio with the correct
  player id. */
  SELECT p.player_id, p.name, COALESCE(w.wins, 0) AS wins, COALESCE(l.losses, 0) AS losses
    FROM players AS p
    LEFT JOIN count_wins AS w
      ON p.player_id = w.player_id
    LEFT JOIN count_losses AS l
      ON p.player_id = l.player_id;

CREATE VIEW standings AS
  /* View selects the required information for playerStandings function: id, name,
  number of wins and number of total matches played for each player from match_stats.
  SUM function is used to total the number of matches played, adding wins and losses
  together, to display round results */
  SELECT m.player_id, m.name, m.wins, SUM(m.wins + m.losses) AS total_matches
    FROM match_stats AS m
    GROUP BY m.player_id, m.name, m.wins
    ORDER BY m.wins DESC;
