from typing import Callable
from ansa import base,constants
from literals import Entities
import logging

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
        
        self.inclu = inclu
        ## coordinate systems 
        self.scs,self.mcss = self._parse_css_name()

        self.SETS = self.get(Entities.SET)
        self.PART = self.get(Entities.PROPERTY)
    
    def get(self,ty:str):
        return base.CollectEntities(self.deck,self.inclu,ty)
    
    # parse INCLUDE, return master and slave cs
    def _parse_css_name(self):
        mcss = []
        scs: base.Entity = None
        CSs = self.get(Entities.COORD)
        # return [cs._name for cs in CSs]
        for cs in CSs:
            assert len(cs._name) > 0, "cs name empty!"
            name_vec = cs._name.split(' ')
            if name_vec[0] == 'S':
                scs = cs
            elif name_vec[0] == 'M':
                mcss.append(cs)
            else:
                logging.debug(CSs)
        
        return scs,mcss



