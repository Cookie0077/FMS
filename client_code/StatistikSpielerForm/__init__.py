from ._anvil_designer import StatistikSpielerFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StatistikSpielerForm(StatistikSpielerFormTemplate):
  def __init__(self, Spieler_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_Player_name.text = f"Statistiken: {Spieler_dict['name']}"
    Player_stats = anvil.server.call("get_Player_stats",Spieler_dict["Spieler_id"])

    self.repeating_panel_Player_stats.items = Player_stats
    # Any code you write here will run before the form opens.
    GPM = anvil.server.call("GetPlayerGoalsPerGame", Spieler_dict["Spieler_id"])
    print(GPM)

    Dates = [row["Datum"] for row in GPM]
    Goals = [row["tore"] for row in GPM]

    lines = go.Scatter(
      x = Dates,
      y = Goals,
      mode='lines+markers', # Punkte für die Spiele, Linien für den Verlauf
      name='Tore',
    )  
    self.plot_Goals_per_Game.data = [lines]

    self.plot_Goals_per_Game.layout.title = "Torausbeute im Verlauf"
    self.plot_Goals_per_Game.layout.xaxis.title = "Spiel"
    self.plot_Goals_per_Game.layout.yaxis.title = "Tore"
    self.plot_Goals_per_Game.layout.xaxis.type = 'category'
    self.plot_Goals_per_Game.layout.plot_bgcolor = '#2c2c2c'
    self.plot_Goals_per_Game.layout.paper_bgcolor = '#2c2c2c'
  
    self.plot_Goals_per_Game.layout.yaxis.dtick = 1 
    self.plot_Goals_per_Game.layout.yaxis.rangemode = 'tozero'
