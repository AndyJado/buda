import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
import glob,random
from ansa import base



if __name__ == "__main__":
    os.system('clear')
    DECK = ansa.constants.LSDYNA
    # time = helpers.NewScript(DECK)
    #-----------------------------------
    # rnid = 3325
    # ppts = buconnect.get_revolute_joint_rigid_pair(DECK,rnid)
    # ppts = buconnect.get_rigid_node_ppts(DECK,13)
    rng = lambda: random.random() * 5000

    ppts = base.CollectEntities(DECK,None,literals.Entities.PROPERTY,filter_visible=True)
    print([i._id for i in ppts])
    for i in ppts:
        eles = base.CollectEntities(DECK,i,literals.Meshes.ELEMENT)
        ansa.base.GeoRotate('MOVE','AUTO_OFFSET',"SAME PART","NONE",rng(),rng(),rng(),rng(),rng(),rng(),rng(),eles)
        ansa.base.GeoTranslate('MOVE','AUTO_OFFSET',"SAME PART","NONE",rng(),rng(),rng(),eles)
        incl = bubase.ents_new_inclu(DECK,eles,'/home/mz/repos/buda/dirty/susp/{}.k'.format(random.randint(1,1000)))
        ansa.base.OutputLSDyna(include=incl)
    


    #-----------------------------------
    # time.end() 
