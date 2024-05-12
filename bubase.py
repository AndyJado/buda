from ansa import base,constants
from literals import Entities,Meshes

## one property, one include.
def dyna_part_a_include(fpath:str) -> base.Entity:
    inclu = base.InputLSDyna(fpath,header="overwrite",new_include="on",create_parameters="on")
    ppts_inclu = base.CollectEntities(constants.LSDYNA,inclu,Entities.PROPERTY,recursive=True)
    num_part = len(ppts_inclu)
    assert num_part == 1, "one include now has {} part!".format(num_part)
    return ppts_inclu[0]

def reveal_unrecogonized_ents(deck:int) -> list[str]:
    ents = base.CollectEntitiesI(deck,None,'__ALL_ENTITIES__')
    meshes_ty = [ty.value for ty in Meshes]
    ents_ty = [ty.value for ty in Entities]
    ents_ty.extend(meshes_ty)
    # return meshes_ty
    return list(set([ent.ansa_type(deck) for ent in ents if ent.ansa_type(deck) not in ents_ty]))
