from ._anvil_designer import VereinsSeiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .SpieleGrid import SpieleGrid 
from .KaderGrid import KaderGrid

Verein_dict = {}
class VereinsSeite(VereinsSeiteTemplate):
  def __init__(self,Vereins_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    Verein_dict.update(Vereins_dict)
    self.label_VereinsName.text = Vereins_dict["Vereinsname"]
    self.image_Vereinslogo.source = Vereins_dict["Logo"]
    self.tabs_Vereine_tab_click(0,"Spiele")
  

  @handle("button_Back", "click")
  def button_Back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("tabs_Vereine", "tab_click")
  def tabs_Vereine_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    if tab_index == 0:
      self.content_panel.clear()
      self.content_panel.add_component(SpieleGrid(Verein_dict["Verein_id"]))
    if tab_index == 1:
      self.content_panel.clear()
      self.content_panel.add_component(KaderGrid(Verein_dict["Verein_id"]))
