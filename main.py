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

    # comment this line to see diff
    # asb.arrest_pair(11,2)

    asb.chains_all()

    for i in asb.chains:
        print(i)

    print(len(asb.chains))
    
    asb.buttn(all)

    #-----------------------------------
    time.end() 