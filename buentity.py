from ansa import base,constants
from typing import Iterable,List,Optional
from literals import *

# extract var to a undefined parameter
def paramrize(deck:int,ent:base.Entity,field:str,name=None):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field,'None')
    name = name or field
    base.CreateEntity(deck,Entities.PARAM, {'Name':name, 'Value': val})
    return ent.set_entity_values(deck,{field: '='+name})

def get_ents_naming(name:str,ty:str,exact=None):
    search = base.NameToEnts(name)
    if exact:
        search = base.NameToEnts(name,match=constants.ENM_EXACT)
    assert search, "no ents naming{}".format(name)
    ents = []
    for ent in search:
        if base.GetEntityType(0, ent) == ty:
            ents.append(ent)
    return ents

def get_entity_by_name(deck:int,name:str,type:str):
    search = base.NameToEnts(name,deck)
    if not search:
        return None
    else:
        ents = []
        for ent in search:
            if base.GetEntityType(deck, ent) == type:
                ents.append(ent)
        if len(ents) == 1:
            return ents[0]     
        elif len(ents) > 1:   
            return ents
