import os
from typing import Iterable
from ansa import base,constants
from literals import Entities,Meshes,Constrains

## one property, one include.
def dyna_a_include(fpath:str) -> base.Entity:
    assert os.path.exists(fpath), "{} not exist!".format(fpath)
    return  base.InputLSDyna(fpath,header="overwrite",new_include="on",create_parameters="on")

def ents_new_inclu(deck:int,ents:Iterable[base.Entity] )-> base.Entity:
    inclu = base.CreateInactiveInclude('','',deck)
    base.LoadInclude(inclu)
    base.AddToInclude(inclu,ents)
    # base.SetEntityCardValues(DECK,inclu,{'Output Path': 'duh'})
    return inclu

# BUG: nodes2ele func returns constrains
def nodes2ppts(deck:int,nodes:list[base.Entity])->list[base.Entity]:
    kwds = [i.value for i in Constrains]

    eles0 = base.NodesToElements(nodes)
    # print(eles0)

    eles:list[base.Entity] = [e for l in eles0.values() for e in l if e.ansa_type(deck) not in kwds]

    # assert len(eles) > 0, 'nodes2ppts ERR: {}'.format(eles0)

    # print('ele from nodes:',eles)
    # tys = set([e.ansa_type(deck) for e in eles])
    # print('types of nodes to elements',tys)

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

def output(fpath:str):
    print("Saving file",fpath)
    base.OutputLSDyna(filename = fpath, mode = "all", disregard_includes = "on",write_comments="off",output_element_thickness='at_element_card')   


def trans_nodes_to_eles(deck:int,nodes:list[base.Entity]):
    elements = base.NodesToElements(nodes)
    ele_selec_ids = set()
    for _, eles in elements.items():
        for ele in eles:
            ele_selec_ids.add(ele._id)

    ele_list = []
    for id in ele_selec_ids:           
        ent = base.GetEntity(deck, "ELEMENT_SHELL", id)
        ele_list.append(ent)
    return ele_list
