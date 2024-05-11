from ansa import base
from literals import *

# extract var to a undefined parameter
def paramrize(deck: int,ent: base.Entity,field:str,name=None):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field,'None')
    name = name or field
    base.CreateEntity(deck,Entities.PARAM, {'Name':name, 'Value': val})
    return ent.set_entity_values(deck,{field: '='+name})

