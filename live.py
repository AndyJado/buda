import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
import glob,random
from ansa import base



if __name__ == "__main__":
    os.system('clear')
    DECK = ansa.constants.LSDYNA
    # time = helpers.NewScript(DECK)
    #-----------------------------------
    rnid = 3325
    ppts = buconnect.get_revolute_joint_rigid_pair(DECK,rnid)
    # ppts = buconnect.get_rigid_node_ppts(DECK,13)
    print(ppts)

    #-----------------------------------
    # time.end() 
