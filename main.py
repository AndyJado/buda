import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs
import glob

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    fps = glob.glob(f'asset/parts/*.key',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    # for i in inclus:
    #     duh = ansa.base.Cog(i)
    #     print(duh)
    eves = [plugs.Eve(DECK,i) for i in inclus]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()

    # for k,v in asb.dps.items():
    #     print(k,v)
    # asb.buttn()
    asb.left_chains()
    asb.realize_next_left()
    asb.realize_next_right()

    #-----------------------------------
    time.end() 