from helpers import *
import ansa
import buconnect,bumesh

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)
    print(plate.ansa_type(DECK))

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    f = lambda: (nodes_all.pop()._id for _ in range(3))

    no,nx,ny = f()
    cys = buconnect.cre_coord_sys_3node(DECK,no,nx,ny)
    ori = buconnect.dp(no)

    d_hole = 30.0

    buconnect.move_along_cs('COPY',cys._id,[20,30,20],[plate])
    buconnect.move_along_cs('COPY',cys._id,[20,0,10],[plate])

    bumesh.openhole(DECK,ori,d_hole)
    
    bolt = buconnect.BoltBuilder(DECK)
    bolt.solid_bolt(d_hole,30.0)
    bolt.apply()
    
