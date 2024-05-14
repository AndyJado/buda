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
    x1,y1,z1 = f()
    cys_m = buconnect.cre_coord_sys_3node(DECK,x1,y1,z1)

    inclu = bubase.ents_new_inclu(DECK,[plate,cys])
    inclu2 = bubase.ents_new_inclu(DECK,[cys_m])

    base.SetEntityCardValues(DECK,cys,{'Name':'S'})

    base.SetEntityCardValues(DECK,cys_m,{'Name':'M'})

    asb = plugs.Assemblr(DECK,[plugs.Eve(DECK,inclu),plugs.Eve(DECK,inclu2)])

    duh = asb.possibles()
    print(duh)

    asb.final()

    time.end()