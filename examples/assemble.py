from helpers import *
import ansa
import buconnect,bumesh,plugs,bubase

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    graph:list[Iterable[str]] = [['(M','M'],['S'],['(S','(M','((M'],['((S']]

    inclus = [random_cs_a_inclu(DECK,nodes_all,i) for i in graph]

    eves = [plugs.Eve(DECK,i) for i in inclus]

    asb = plugs.Assemblr(DECK,eves)

    # duh = asb.recurr()
    # print(duh)

    print(asb)

    time.end()