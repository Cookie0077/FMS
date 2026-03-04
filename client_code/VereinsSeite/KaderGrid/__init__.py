from ._anvil_designer import KaderGridTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class KaderGrid(KaderGridTemplate):
  def __init__(self,Verein_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    Spieler = anvil.server.call('query_database_getSpieler', f'{Verein_id}')
    self.repeating_panel_Spieler.items = Spieler
  
