from helpers import *
import ansa
import buconnect,bumesh,plugs,bubase

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)
    
    no,nx,ny = (228,205,152)
    o2,x2,y2 = (9,10,11) 
    cys = buconnect.cre_coord_sys_3node(DECK,no,nx,ny)
    cys_m = buconnect.cre_coord_sys_3node(DECK,o2,x2,y2)

    inclu = bubase.ents_new_inclu(DECK,[plate,cys])
    inclu2 = bubase.ents_new_inclu(DECK,[cys_m])

    base.SetEntityCardValues(DECK,cys,{'Name':'S'})

    base.SetEntityCardValues(DECK,cys_m,{'Name':'M'})

    asb = plugs.Assemblr(DECK,[plugs.Eve(DECK,inclu),plugs.Eve(DECK,inclu2)])

    duh = asb.possibles()
    print(duh)

    asb.final()

    time.end()