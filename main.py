import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs,literals
import glob
from ansa import base

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    fps = glob.glob(f'dirty/susp/after_cs/improve/3lyrs/*.k',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    all = base.CollectEntities(DECK,None,literals.Entities.ALL)

    eves = [plugs.Eve(DECK,i) for i in inclus]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()

    asb.chains_all()

    # must_have_pairs = [(9,10),(1,15),(5,13),(11,None)]

    must_have_pairs = [(None,8),(15,1),(12,14),(11,None)]

    for par in must_have_pairs[0:0]:
        asb.elect_pair(par[0],par[1])

    # for i in asb.chains:
    #     print(i)

    most_pairs = asb.pair_counter()

    leasts = [i[0] for i in sorted(most_pairs.items(), key=lambda item: item[1])]
    print('leasts_pairs',leasts)

    # mosts = most_pairs.most_common(3)
    # print('mosts',mosts)

    print('chains left:',len(asb.chains))
    
    asb.buttn(all)

    #-----------------------------------
    time.end() 