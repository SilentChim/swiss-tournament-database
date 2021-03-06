#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
# Used to provide access to your database via a library of functions which can
# add, delete or query data in your database to another python program.
# Remember that when you define a function, it does not execute, it simply means
# the function is defined to run a specific set of instructions when called.

import psycopg2


def connect():
  """Connect to the PostgreSQL database.  Returns a database connection."""
  return psycopg2.connect("dbname=tournament")


def deleteMatches():
  """Remove all the match records from the database."""
  DB = connect()
  c = DB.cursor()
  c.execute("DELETE FROM matches")
  DB.commit()
  DB.close()


def deletePlayers():
  """Remove all the player records from the database."""
  DB = connect()
  c = DB.cursor()
  c.execute("DELETE FROM players")
  DB.commit()
  DB.close()


def countPlayers():
  """Returns the number of players currently registered."""
  DB = connect()
  c = DB.cursor()
  sql = """SELECT COUNT(*) AS num FROM players"""
  c.execute(sql,)
  players = c.fetchone()[0]
  DB.close()
  return players


def registerPlayer(name):
  """Adds a player to the tournament database.

  The database assigns a unique serial id number for the player.  (This
  should be handled by your SQL database schema, not in your Python code.)

  Args:
    name: the player's full name (need not be unique).
  """
  DB = connect()
  c = DB.cursor()
  player = """INSERT INTO players(name) VALUES(%s) RETURNING player_id;"""
  c.execute(player, (name,))
  player_id = c.fetchone()[0]
  DB.commit()
  DB.close()


def playerStandings():
  """Returns a list of the players and their win records, sorted by wins.

  The first entry in the list should be the player in first place, or a player
  tied for first place if there is currently a tie.

  Returns:
    A list of tuples, each of which contains (id, name, wins, matches):
      id: the player's unique id (assigned by the database)
      name: the player's full name (as registered)
      wins: the number of matches the player has won
      matches: the number of matches the player has played
  """
  DB = connect()
  c = DB.cursor()
  standings = """SELECT * FROM standings;"""
  c.execute(standings,)
  ranks = []
  for row in c.fetchall():
      ranks.append(row)
  DB.close()
  return ranks


def reportMatch(winner, loser):
  """Records the outcome of a single match between two players.

  Args:
    winner:  the id number of the player who won
    loser:  the id number of the player who lost
  """
  DB = connect()
  c = DB.cursor()
  sql = """INSERT INTO matches (winner, loser) VALUES (%s, %s);"""
  c.execute(sql, (winner, loser,))
  DB.commit()
  DB.close()

def swissPairings():
  """Returns a list of pairs of players for the next round of a match.

  Assuming that there are an even number of players registered, each player
  appears exactly once in the pairings.  Each player is paired with another
  player with an equal or nearly-equal win record, that is, a player adjacent
  to him or her in the standings.

  Returns:
    A list of tuples, each of which contains (id1, name1, id2, name2)
      id1: the first player's unique id
      name1: the first player's name
      id2: the second player's unique id
      name2: the second player's name
  """

  # Combines even and odd rows from descending standings into tuples

  standings = playerStandings()
  pairings = []

  for player1, player2 in zip(standings[0::2], standings[1::2]):
        pairings.append((player1[0], player1[1], player2[0], player2[1]))

  return pairings
