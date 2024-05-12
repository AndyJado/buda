from ansa import base,constants
from literals import Entities

## one property, one include.
def dyna_part_a_include(fpath:str) -> base.Entity:
    inclu = base.InputLSDyna(fpath,header="overwrite",new_include="on",create_parameters="on")
    ppts_inclu = base.CollectEntities(constants.LSDYNA,inclu,Entities.PROPERTY,recursive=True)
    num_part = len(ppts_inclu)
    assert num_part == 1, "one include now has {} part!".format(num_part)
    return ppts_inclu[0]
