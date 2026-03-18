from ._anvil_designer import StatistikSpielerFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

ThisSpieler_dict = {}
class StatistikSpielerForm(StatistikSpielerFormTemplate):
  def __init__(self, Spieler_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_Player_name.text = f"Statistiken: {Spieler_dict['name']}"
    Player_stats = anvil.server.call("get_Player_stats",Spieler_dict["Spieler_id"])
    ThisSpieler_dict.update(Spieler_dict)
    self.repeating_panel_Player_stats.items = Player_stats
    # Any code you write here will run before the form opens.
    GPM = anvil.server.call("GetPlayerGoalsPerGame", Spieler_dict["Spieler_id"])
    print(GPM)

    Dates = [row["Gegner"] for row in GPM]
    Goals = [row["tore"] for row in GPM]

    lines = go.Scatter(
      x = Dates,
      y = Goals,
      mode='lines+markers',
      name='Tore',
    )  
    self.plot_Goals_per_Game.data = [lines]

    self.plot_Goals_per_Game.layout.title = "Torausbeute im Verlauf"
    self.plot_Goals_per_Game.layout.xaxis.title = "Spiel"
    self.plot_Goals_per_Game.layout.yaxis.title = "Tore"
    self.plot_Goals_per_Game.layout.xaxis.type = 'category'
    self.plot_Goals_per_Game.layout.plot_bgcolor = '#2c2c2c'
    self.plot_Goals_per_Game.layout.paper_bgcolor = '#2c2c2c'
    self.plot_Goals_per_Game.layout.xaxis.color = '#7438ef'
    self.plot_Goals_per_Game.layout.yaxis.color =  '#7438ef'
  
    self.plot_Goals_per_Game.layout.yaxis.dtick = 1 
    self.plot_Goals_per_Game.layout.yaxis.rangemode = 'tozero'
    self.plot_Goals_per_Game.layout.margin = dict(
      l=50,  # Links
      r=50,  # Rechts
      t=50,  # Oben
      b=200  
    )

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Vereins_dict = anvil.server.call("query_database_getSingleVerein",ThisSpieler_dict["Verein_id"])
    open_form("VereinsSeite",Vereins_dict)
