import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
import glob,random



if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    
    fps = glob.glob(f'asset/teile/*.key',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    rng = lambda: random.random() * 5000

    for i in inclus:
        tys = [literals.Entities.COORD,literals.Meshes.ELEMENT]
        to_tran = ansa.base.CollectEntities(DECK,i,tys)
        ansa.base.GeoTranslate(
        'MOVE',
        'AUTO_OFFSET',
        "SAME PART",
        "NONE", # set will simply move with
        rng(),
        rng(),
        rng(),
        to_tran,
        )
        ansa.base.OutputLSDyna(include=i)

    #-----------------------------------
    time.end() 
