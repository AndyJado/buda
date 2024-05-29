from helpers import *
import ansa
import buconnect,bumesh,bucreate,buentity,random
from time import sleep

DECK = ansa.constants.LSDYNA

# if scripts fails, try rerun.
if __name__ == "__main__":
    timing = NewScript(DECK)

    plate = a_plate_mesh(DECK)

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    f = lambda: (nodes_all.pop()._id for _ in range(3))

    no,nx,ny = f()
    cys = buconnect.cre_coord_sys_3node(DECK,no,nx,ny)
    ori = buconnect.dp(no)

    d_hole = 30.0

    buconnect.copy_along_cs(cys._id,[20,30,20],[plate])
    buconnect.copy_along_cs(cys._id,[20,0,10],[plate])

    for i in range(0,2):
        se = bucreate.cre_set(0,nodes_all.pop(),i)

    base.OutputLSDyna('temp.k')
    NewScript(DECK)
    base.InputLSDyna('temp.k')

    for i in range(0,2):
        sets = buentity.get_ents_naming(str(i),literals.Entities.SET,True)
        for se in sets:
            nds = base.CollectEntities(0,se,literals.Meshes.NODE)
            base.DeleteEntity(se)
            to_cre = bucreate.cre_set(0,nds)
            h_id = bucreate.cre_hole_from_set(0,to_cre._id,d_hole+random.random()*1e-4,50)
            bucreate.cre_bolt_auto(DECK,28.0-10*i,30-10*i,'asset/mat24.key',h_id)
 
    timing.end()
