from ._anvil_designer import StatistikFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

GMatch_dict = {}
class StatistikForm(StatistikFormTemplate):
  def __init__(self, Match_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Stat_dict = anvil.server.call("get_Player_Rating",Match_dict["Match_id"],Match_dict["Verein_id"])
    print(Stat_dict)
    GMatch_dict.update(Match_dict)
    namen =  [row['name'] for row in Stat_dict]
    ratings = [row['rating'] for row in Stat_dict]

    balken = go.Bar(
      x = ratings,         # x-Achse: Die Länge der Balken (Rating)
      y = namen,           # y-Achse: Die Beschriftung (Spielername)
      orientation = 'h',   # 'h' steht für horizontal
      marker_color = '#1f77b4'  # Ein klassisches Blau
    )

    self.Player_ratings.data = [balken]
    self.Player_ratings.layout.title = "Player Ratings"
    self.Player_ratings.layout =dict(l=150)
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Vereins_dict = anvil.server.call("query_database_getSingleVerein",GMatch_dict["Verein_id"])
    print(Vereins_dict)
    open_form('VereinsSeite',Vereins_dict)
