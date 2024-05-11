from ansa import base
from literals import *

## FIXME: not test yet
def get_ent_from_name(deck:int,type:str,name:str) -> base.Entity:
    ents = base.CollectEntitiesI(deck,None,type)
    ents_with_name = [ent for ent in ents if ent._name == name]
    num = len(ents_with_name)
    assert num == 1, "ERROR: Type {} has {} entities with name {}!".format(type,num,name)
    return ents_with_name[0]

# extract var to a undefined parameter
def paramrize(deck: int,ent: base.Entity,field:str,name=None):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field,'None')
    name = name or field
    base.CreateEntity(deck,Entities.PARAM, {'Name':name, 'Value': val})
    return ent.set_entity_values(deck,{field: '='+name})

