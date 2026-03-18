import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import plotly.graph_objects as go


@anvil.server.callable
def query_database_getLiga():
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute("SELECT name FROM Liga").fetchall()
  return result

@anvil.server.callable
def query_database_getSingleVerein(Verein_id:str):
  sql = f"""SELECT Verein.Verein_id , Verein.Name AS Vereinsname, Verein.Gründungsjahr AS GruendungsJahr, 
        Verein.Stadion_Kapazität AS Kapazitaet, Verein.Logo AS Logo FROM Verein
        WHERE Verein_id = '{Verein_id}'
        """
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchone()
  return dict(result)


@anvil.server.callable
def query_database_getVereine(liga: str):

  sql = f"""SELECT Verein.Verein_id , Verein.Name AS Vereinsname, Verein.Gründungsjahr AS GruendungsJahr, 
        Verein.Stadion_Kapazität AS Kapazitaet, Verein.Logo AS Logo FROM Verein
        JOIN Liga
        ON Verein.Liga_id = Liga.Liga_id
        WHERE Liga.Name = '{liga}';
        """
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
  return [dict(row) for row in result]


@anvil.server.callable
def query_database_getSpieler(Verein_id: str):
  sql = f""" SELECT Spieler.Spieler_Nummer AS nummer, Spieler.Vorname || " " ||
    Spieler.Nachname AS name, Spieler.Marktwert AS marktwert, Spieler.Position 
    AS position, Spieler.Spieler_id AS Spieler_id FROM Spieler
    JOIN Verein_Spieler
    ON Verein_Spieler.Spieler_id = Spieler.Spieler_id
    WHERE Verein_Spieler.Verein_id ='{Verein_id}'; """

  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def query_database_getMatch(Verein_id:str):
    sql = f""" SELECT DISTINCT Match.Datum AS datum, Match.Heimmannschaft as heim, Match.Auswärtsmannschaft
    AS auswaerts, (Match.Tore_Heim || '-' || Match.Tore_Gast) AS ergebnis,Verein.Verein_id, Match.Match_id AS Match_id FROM Match
    JOIN Spieler_Statistik 
    ON Spieler_Statistik.Match_id = Match.Match_id
    JOIN Spieler
    ON Spieler.Spieler_id  = Spieler_Statistik.Spieler_id
    JOIN Verein_Spieler
    On Verein_Spieler.Spieler_id = Spieler.Spieler_id
    JOIN Verein 
    ON Verein.Verein_id = Verein_Spieler.Verein_id
    WHERE Verein.Verein_id = '{Verein_id}';"""
    with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchall()
    return [dict(row) for row in result]


@anvil.server.callable
def get_Player_Rating(Match_id: str,Verein_id):
    sql = f""" SELECT  Spieler.Vorname || " " ||
    Spieler.Nachname || "  " AS name, Spieler_Statistik.Rating AS rating, Spieler_Statistik.Tore AS tore,
    Spieler_Statistik.Gelbe_Karten AS gelbe_karte, Spieler_Statistik.rote_karten AS rote_karte FROM 
	  Match
	  Join Spieler_Statistik
	  ON Match.Match_id = Spieler_Statistik.Match_id
	  JOIN Spieler 
	  ON Spieler_Statistik.Spieler_id = Spieler.Spieler_id
	  JOIN Verein_Spieler 
	  ON Verein_Spieler.Spieler_id = Spieler.Spieler_id
  	JOIN Verein 
	  ON Verein_Spieler.Verein_id = Verein.Verein_id
	  WHERE Match.Match_id = '{Match_id}' and  Verein.Verein_id = '{Verein_id}' """
  
    with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchall()
    return [dict(row) for row in result]

@anvil.server.callable
def GetPlayerGoalsPerGame(Spieler_id:str) :
  sql = f"""SELECT Spieler_Statistik.Tore AS tore,  Match.Auswärtsmannschaft AS Gegner FROM Spieler_Statistik
        JOIN Match 
        ON Spieler_Statistik.Match_id = Match.Match_id
          WHERE Spieler_Statistik.Spieler_id = '{Spieler_id}';"""
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
  return [dict(row) for row in result]
  

@anvil.server.callable
def get_Player_stats(Spieler_id) :
  sql = f""" SELECT sum(Tore) AS ges_tore, count(STATS_id) AS ges_matche, sum(Gelbe_Karten)
      As ges_gelbe, sum(Rote_Karten) AS ges_rote, avg(Rating) AS avg_rating FROM Spieler_Statistik
      WHERE Spieler_id = '{Spieler_id}';"""

  
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(sql).fetchall()
  return [dict(row) for row in result]