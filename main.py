import ansa,logging,sys,gc,os
import buconnect,bumesh,helpers,bubase,plugs,literals
import glob
from ansa import base
import random

def susp_asb(dir:str):

    dir1 = os.path.join(dir,f'*.k')
    output = 'dirty/susp.k'
    fps = glob.glob(dir1,recursive=True)
    inclus = [bubase.dyna_a_include(p) for p in fps]
    all = base.CollectEntities(DECK,None,literals.Entities.ALL)
    eves = [plugs.Eve(DECK,i) for i in inclus]
    asb = plugs.Assemblr(DECK,eves) 
    asb.possi_d_all()
    asb.chains_all()
    # FIXME: playing index
    must_have_pairs = [(1,15)]
    for par in must_have_pairs[0:]:
        asb.elect_pair(par[0],par[1])
    assert len(asb.chains) <= 1, "asemble has more than 1 poss!"    
    print('realizing assembly chian:', asb.chains[0])

    asb.realize_chain_id(0)
    helpers.write_ents(all,output)

    return output

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    truck_dir = 'asset/parts'
    asb = helpers.assemble_a_dir(DECK,truck_dir) 
    asb.buttn()
    #-----------------------------------
    time.end() 