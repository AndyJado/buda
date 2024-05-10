from enum import Enum
from ansa import base

class GenEnts(str, Enum):
    PART: str = 'ANSAPART'
    PROPERTY: str = '__PROPERTIES__'
    MATERIAL: str = '__MATERIALS__'
    SET: str = 'SET'
    CONTACT: str = 'CONTACT'
    SEGMENT: str = 'SEGMENT'

class Meshes(str, Enum):
    NODE: str = 'NODE'
    ELEMENT: str = '__ELEMENTS__'
    SOLID: str = 'ELEMENT_SOLID'
    SHELL: str = 'ELEMENT_SHELL'

class DynaCards(str, Enum):
    SHELL: str= 'SECTION_SHELL'
    MAT1: str = 'MAT1 MAT_ELASTIC'
 

class Node():
    def __init__(self,deck:int,nid:int) -> None:
        self.card = base.Entity(deck,nid,Meshes.NODE).card_fields(deck,True)
    
    def coord(self):
        x:float = self.card.get('X')
        y:float = self.card.get('Y')
        z:float = self.card.get('Z')
        return (x,y,z)

# extract var to a undefined parameter
def paramrize(deck: int,ent: base.Entity,field:str,name=None):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field,'None')
    name = name or field
    base.CreateEntity(deck,"A_PARAMETER", {'Name':name, 'Value': val})
    return ent.set_entity_values(deck,{field: '='+name})

