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
    AS position FROM Spieler
    JOIN Verein_Spieler
    ON Verein_Spieler.Spieler_Nummer = Spieler.Spieler_Nummer
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
    ON Spieler.Spieler_Nummer  = Spieler_Statistik.Spieler_Nummer
    JOIN Verein_Spieler
    On Verein_Spieler.Spieler_Nummer = Spieler.Spieler_Nummer
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
    Spieler.Nachname AS name, Spieler_Statistik.Rating AS rating FROM 
	  Match
	  Join Spieler_Statistik
	  ON Match.Match_id = Spieler_Statistik.Match_id
	  JOIN Spieler 
	  ON Spieler_Statistik.Spieler_Nummer = Spieler.Spieler_Nummer
	  JOIN Verein_Spieler 
	  ON Verein_Spieler.Spieler_Nummer = Spieler.Spieler_Nummer
  	JOIN Verein 
	  ON Verein_Spieler.Verein_id = Verein.Verein_id
	  WHERE Match.Match_id = '{Match_id}' and  Verein.Verein_id = '{Verein_id}' """
  
    with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
      conn.row_factory = sqlite3.Row
      cur = conn.cursor()
      result = cur.execute(sql).fetchall()
    return [dict(row) for row in result]

  

 