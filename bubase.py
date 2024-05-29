from typing import Iterable
from ansa import base,constants
from literals import Entities,Meshes,Constrains

## one property, one include.
def dyna_a_include(fpath:str) -> base.Entity:
    return  base.InputLSDyna(fpath,header="overwrite",new_include="on",create_parameters="on")

def ents_new_inclu(deck:int,ents:Iterable[base.Entity]) -> base.Entity:
    inclu = base.CreateInactiveInclude('','',deck)
    base.LoadInclude(inclu)
    base.AddToInclude(inclu,ents)
    # base.SetEntityCardValues(DECK,inclu,{'Output Path': 'duh'})
    return inclu

def nodes2ppts(deck:int,nodes:list[base.Entity])->list[base.Entity]:
    kwds = [i.value for i in Constrains]

    eles0 = base.NodesToElements(nodes)
    print(eles0)

    eles:list[base.Entity] = [e for l in eles0.values() for e in l if e.ansa_type(deck) not in kwds]

    print('ele from nodes:',eles)

    # tys = set([e.ansa_type(deck) for e in eles])
    # print(tys)

    ppts = [e.card_fields(deck,True)['PID'] for e in eles]
    # print('ppts:',list(set(ppts)))

    return list(set(ppts))

def reveal_unrecogonized_ents(deck:int) -> list[str]:
    ents = base.CollectEntitiesI(deck,None,'__ALL_ENTITIES__')
    meshes_ty = [ty.value for ty in Meshes]
    ents_ty = [ty.value for ty in Entities]
    ents_ty.extend(meshes_ty)
    # return meshes_ty
    return list(set([ent.ansa_type(deck) for ent in ents if ent.ansa_type(deck) not in ents_ty]))
