from ._anvil_designer import StartseiteTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    Ligen = anvil.server.call('query_database','SELECT name FROM Liga')
    Ligen = [ entry[0] for entry in Ligen]
    self.drop_down_Ligen.items = Ligen
    self.drop_down_Ligen_change()

  @handle("drop_down_Ligen", "change")
  def drop_down_Ligen_change(self, **event_args):
    sql = f"""SELECT Verein.Name AS Vereinsname, Verein.Gründungsjahr AS GruendungsJahr, 
        Verein.Stadion_Kapazität AS Kapazitaet FROM Verein
        JOIN Liga
        ON Verein.Liga_id = Liga.Liga_id
        WHERE Liga.Name = '{self.drop_down_Ligen.selected_value}';
        """

    Vereine = anvil.server.call('query_database_dict',sql)

    self.repeating_panel_Vereine.items = Vereine
    

    
