from helpers import *
import ansa
import buconnect,bumesh,plugs,bubase

DECK = ansa.constants.LSDYNA


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh(DECK)

    nodes_all = set(base.CollectEntities(DECK,None,literals.Meshes.NODE))

    # graph:list[Iterable[str]] = [['(M','M'],['S'],['(S','(M','((M'],['((S'],]

    graph:list[Iterable[str]] = [['M'],['M'],['S'],['S'],['S','M','M']]


    inclus = [random_cs_a_inclu(DECK,nodes_all,i) for i in graph]

    eves = [plugs.Eve(DECK,i) for i in inclus]
    
    asb = plugs.Assemblr(DECK,eves)
    print(asb)

    d0 = asb.layers[0]
    M = [css for l in d0 if l.ty() == 'M' for css in l.mcss]

    I = [(l.scs,l.mcss) for l in d0 if l.ty() == 'I']

    i_dict = {}
    for (s,ms) in I:
        i_dict.update({s:ms})

    S = [l.scs for l in d0 if l.ty() == 'S']
  
    print(i_dict)

    time.end()