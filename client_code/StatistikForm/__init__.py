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

    self.Player_ratings.layout.title = "Player Ratings"
    self.Player_ratings.layout.xaxis.title = "Rating"
    self.Player_ratings.layout.yaxis.title = "Spieler"
    self.Player_ratings.layout.paper_bgcolor = '#2c2c2c'
    self.Player_ratings.layout.plot_bgcolor = '#2c2c2c'
    self.Player_ratings.layout.font = dict(color="white") 
    self.Player_ratings.layout.margin = dict(l=150, r=50, t=50, b=80)

    balken = go.Bar(
      x = ratings,        
      y = namen,           
      orientation = 'h',   
      marker_color = '#1f77b4'  
    )
    self.Player_ratings.data = [balken]
  
    self.repeating_panel_player_stats.items = Stat_dict


  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Vereins_dict = anvil.server.call("query_database_getSingleVerein",GMatch_dict["Verein_id"])
    print(Vereins_dict)
    open_form('VereinsSeite',Vereins_dict)
