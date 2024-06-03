from helpers import *
import ansa
import buconnect,bumesh
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

    sleep(0.3)
    buconnect.copy_along_cs(cys._id,[20,30,20],[plate])
    sleep(0.3)
    buconnect.copy_along_cs(cys._id,[20,0,10],[plate])
    sleep(0.3)
    bumesh.openhole(DECK,ori,d_hole)
    sleep(0.3)
    bolt = buconnect.BoltBuilder(DECK)
    bolt.solid_bolt(d_hole,30.0)
    bolt.apply()
    
    timing.end()
