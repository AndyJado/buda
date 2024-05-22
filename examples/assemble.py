from helpers import *
import ansa
import buconnect,bumesh,plugs,bubase

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    ## this should not work 
    # graph:list[Iterable[str]] = [['(M','M'],['S'],['(S','(M','((M'],['((S'],]

    graph:list[Iterable[str]] = [['M','M'],['M'],['S'],['S'],['S','M','M'],['S','M']]

    # graph:list[Iterable[str]] = [['M'],['M'],['S'],['S'],['S','M']]

    inclus = [random_cs_a_inclu(DECK,nodes_all,i) for i in graph]

    eves = [plugs.Eve(DECK,i) for i in inclus]
    
    asb = plugs.Assemblr(DECK,eves)
    asb.possi(0)

    # print([str(i) for i in asb.dps[0]])

    pid = asb.realize_left(0,0)

    # print('posi id:',pid)
 
    time.end()