from ._anvil_designer import VereinsSeiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class VereinsSeite(VereinsSeiteTemplate):
  def __init__(self,Vereins_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_VereinsName.text = Vereins_dict["Vereinsname"]

  @handle("button_Back", "click")
  def button_Back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
