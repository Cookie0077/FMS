import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

@anvil.server.callable
def query_database_getLiga():
  with sqlite3.connect(data_files["fussball_manager.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute("SELECT name FROM Liga").fetchall()
  return result
  
@anvil.server.callable
def query_database_getVereine(liga: str):

  sql = f"""SELECT Verein.Name AS Vereinsname, Verein.Gründungsjahr AS GruendungsJahr, 
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
def query_database_getVereine(Verein: str):

  