from helpers import *
import ansa
import buconnect,bumesh,plugs,bubase

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    f = lambda: (nodes_all.pop()._id for _ in range(3))

    x,y,z = f()
    cys = buconnect.cre_coord_sys_3node(DECK,x,y,z)


    x,y,z = f()
    cys2 = buconnect.cre_coord_sys_3node(DECK,x,y,z)

    inclu = bubase.ents_new_inclu(DECK,[plate,cys,cys2])

    base.SetEntityCardValues(DECK,cys,{'Name':'(((S'})
    base.SetEntityCardValues(DECK,cys2,{'Name':'S'})

    eve = plugs.Eve(DECK,inclu)

    for e in eve.lyrs:
        print(e)

    time.end()