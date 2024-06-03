import ansa,logging,sys,gc,os
import buconnect,bumesh,helpers,bubase,plugs,literals
import glob
from ansa import base
import random

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    truck_dir = 'examples/truck_assemble/truck'
    rear_susp_dir = 'examples/truck_assemble/susp-3lyrs'
    rear_output = 'examples/truck_assemble/truck/rear-susp.k'

    rear_asb = helpers.dir_a_asb(DECK,rear_susp_dir)

    rear_asb.try_final()

    to_sym = base.CollectEntities(DECK,rear_asb.inclus,literals.Meshes.ELEMENT)

    #TODO: collect from set
    mirror_nodes = (11271,11272,11273)

    buconnect.miror_ents_3_nodes(DECK,to_sym,mirror_nodes)
    helpers.write_ents_with_ref(rear_asb.inclus,rear_output)
    base.DeleteEntity(base.CollectEntities(DECK,rear_asb.inclus,literals.Entities.ALL))

    truck_asb = helpers.dir_a_asb(DECK,truck_dir) 
    truck_asb.try_final()

    # truck_asb.buttn()
    #-----------------------------------
    time.end() 