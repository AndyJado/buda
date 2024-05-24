import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs,literals
import glob
from ansa import base

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    fps = glob.glob(f'asset/parts/*.key',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    all = base.CollectEntities(DECK,None,literals.Entities.ALL)

    eves = [plugs.Eve(DECK,i) for i in inclus]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()
    asb.chains_all()

    # print(len(asb.chains))
    
    # asb.buttn(all)
    # print(asb.chains)

    # asb.realize_chain_id(3)

    # gut = ([(4, 11), (2, 13)], [(1, 9)], [(6, 5), (8, 10)],[(14, 3), (7, 12)])

    gut = ([(4, 11), (2, 13)], [(1, 9)],)
    for c in gut:
        for p in c:
            asb.realize_pair(p)




    #-----------------------------------
    time.end() 