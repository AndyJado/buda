import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs,literals
import glob
from ansa import base

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    fps = glob.glob(f'dirty/susp/after_cs/*.k',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    all = base.CollectEntities(DECK,None,literals.Entities.ALL)

    eves = [plugs.Eve(DECK,i) for i in inclus]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()

    asb.chains_all()

    must_have_pairs = [(1,12),(7,8),(3,5)]
    for par in must_have_pairs:
        asb.elect_pair(par[0],par[1])

    # for i in asb.chains:
    #     print(i)
    most_pairs = asb.most_pair()
    print('most_pairs',most_pairs)

    print('chains left:',len(asb.chains))
    
    asb.buttn(all)

    #-----------------------------------
    time.end() 