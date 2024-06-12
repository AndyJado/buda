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
        helpers.write_ents_with_ref(to_tran,r'/home/mz/repos/buda/dirty/susp/{}.k'.format(random.randint(0,1000)))

# DANGER!
def random_move_inclu():
    inclus = base.CollectEntities(DECK,None,literals.Entities.INCLUDE)
    tys = [literals.Entities.COORD,literals.Meshes.ELEMENT]

    for icl in inclus:
        to_tran = ansa.base.CollectEntities(DECK,icl,tys)
        helpers.random_move_ents(to_tran,500)
        base.OutputLSDyna(include=icl)

def a_window_a_inclu(dir:str):
    dir1 = os.path.join(dir,f'*.key')
    dir2 = os.path.join(dir,f'*.k')
    fps = glob.glob(dir1) + glob.glob(dir2)
    for f in fps:
        base.InputLSDyna(f,model_action="new_model_in_new_window")

if __name__ == "__main__":
    # os.system('clear')
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    cup_dir ='asset/cup'
    cup_asb = helpers.dir_a_asb(DECK,cup_dir)
    cup_asb.try_final()
    #-----------------------------------
    time.end()
