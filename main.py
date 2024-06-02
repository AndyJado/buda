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

    asb.elect_named()
    
    remain_possi = len(asb.chains)
    print('remain_possi', remain_possi)
    # asb.buttn()
    # assert len(asb.chains) <= 1, "asemble has more than 1 poss!"    
    # print('realizing assembly chian:', asb.chains[0])

    # asb.realize_chain_id(0)
    # helpers.write_ents(all,output)


    return output

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    truck_dir = 'dirty/truck'
    rear_susp_dir = 'dirty/susp/after_cs/improve/3lyrs'
    rear_output = 'dirty/truck/rear-susp.k'
    # out1 = 'dirty/truck/'
    rear_asb = helpers.dir_a_asb(DECK,rear_susp_dir)
    rear_asb.try_final()

    helpers.write_ents_with_ref(rear_asb.inclus,rear_output)
    base.DeleteEntity(base.CollectEntities(DECK,rear_asb.inclus,literals.Entities.ALL))
    truck_asb = helpers.dir_a_asb(DECK,truck_dir) 
    truck_asb.try_final()

    # truck_asb.buttn()
    #-----------------------------------
    time.end() 