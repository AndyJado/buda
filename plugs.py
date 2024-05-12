from typing import Callable
from ansa import base,constants
import literals

def unplug_meshes(deck:int):
    nodes = base.CollectEntitiesI(deck,None,"NODE") # ELEMENT will delete parts!
    base.DeleteEntity(nodes,force=True)

def paramlater(deck:int, ent: base.Entity, field:str,name:str):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field) or  0 # 'None' if none
    param = base.CreateEntity(deck,"A_PARAMETER", {'Name':name})
    return ent.set_entity_values(deck,{field: '='+name})


## right hand rule for coordinate sys everywhere
##
class Eve():
    def __init__(self,path:str) -> None:
        self.deck = constants.LSDYNA
        inclu = base.InputLSDyna(path,header='overwrite',new_include='on',create_parameters='on')
        ## coordinate systems 
        self.inclu = inclu
        # self.CSS = base.CollectEntities(self.deck,inclu,literals.Entities.COORD)
        self.CSS = self.get(literals.Entities.COORD)
        self.SETS = base.CollectEntities(self.deck,inclu,literals.Entities.SET)
        self.PART = base.CollectEntities(self.deck,inclu,literals.Entities.PROPERTY)
    
    def get(self,ty:str):
        return base.CollectEntities(self.deck,self.inclu,ty)
    
    def _parse_css_name():
        pass
