from ansa import base,constants
from literals import Entities

## one property, one include.
def dyna_part_a_include(fpath:str) -> base.Entity:
    inclu = base.InputLSDyna(fpath,header="overwrite",new_include="on",create_parameters="on")
    ppts_inclu = base.CollectEntities(constants.LSDYNA,inclu,Entities.PROPERTY,recursive=True)
    assert len(ppts_inclu) == 1, "one include, one part!"
    return ppts_inclu[0]

