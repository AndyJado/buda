import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
import glob,random
from ansa import base

def visble_ents_random_inclu():
    ppts = base.CollectEntities(DECK,None,literals.Entities.PROPERTY,filter_visible=True)
    
    for ppt in ppts:
        to_tran = base.CollectEntities(DECK,ppt,literals.Meshes.ELEMENT)
        bubase.ents_new_inclu(DECK,to_tran)
        helpers.random_move_ents(to_tran,500)
        helpers.write_ents(to_tran,r'/home/mz/repos/buda/dirty/susp/{}.k'.format(random.randint(0,1000)))

def random_move_inclu():
    inclus = base.CollectEntities(DECK,None,literals.Entities.INCLUDE)
    tys = [literals.Entities.COORD,literals.Meshes.ELEMENT]

    for icl in inclus:
        to_tran = ansa.base.CollectEntities(DECK,icl,tys)
        helpers.random_move_ents(to_tran,500)
        base.OutputLSDyna(include=icl)


if __name__ == "__main__":
    os.system('clear')
    DECK = ansa.constants.LSDYNA
    #-----------------------------------
    random_move_inclu()
    #-----------------------------------
