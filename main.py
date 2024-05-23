import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    rail_path = r'asset/4m-model.key'
    spacer_path =r'asset/spacer.key'
    ballar_path ='asset/stand.key'

    fps = [rail_path,spacer_path,ballar_path]

    inclus = [plugs.Eve(DECK,bubase.dyna_a_include(p)) for p in fps]
 
    asb = plugs.Assemblr(DECK,inclus) 

    asb.possi_d_all()

    asb.realize_all()

    #-----------------------------------
    time.end() 