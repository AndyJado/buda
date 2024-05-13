import ansa,logging,sys
import buconnect,bumesh,helpers,bubase,plugs




if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    rail_path = r'asset/4m-model.key'
    spacer_path =r'asset/spacer.key'
    rail = plugs.Eve(DECK,rail_path)
    spacer = plugs.Eve(DECK,spacer_path)
    ballar = plugs.Eve(DECK,'asset/stand.key')
 
    asb = plugs.Assemblr(DECK,[rail,spacer,ballar]) 
    # duh = asb._possibles()
    duh = asb.final()
    print('duh:',duh)

    #-----------------------------------
    time.end()