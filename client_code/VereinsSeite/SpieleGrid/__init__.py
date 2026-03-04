from ._anvil_designer import SpieleGridTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SpieleGrid(SpieleGridTemplate):
  def __init__(self,Verein_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Spiele = anvil.server.call('query_database_getMatch',f'{Verein_id}')
    self.repeating_panel_Spiele.items = Spiele
