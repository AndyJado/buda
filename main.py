import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs
import glob

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    fps = glob.glob(f'asset/teile/*.key',recursive=True)

    inclus = [bubase.dyna_a_include(p) for p in fps]

    # for i in inclus:
    #     duh = ansa.base.Cog(i)
    #     print(duh)
    eves = [plugs.Eve(DECK,i) for i in inclus]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()

    # asb.buttn()
    # asb.realize_all()

    #-----------------------------------
    time.end() 