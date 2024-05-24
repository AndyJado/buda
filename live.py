import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
import glob,random



if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------
    pack = [['M','M'],['S','(S'],['M','S'],['(M']]

    inclus = [helpers.white_mouse_a_inclu(DECK,helpers.draw_rec(100,100),i) for i in pack]
    eves = [plugs.Eve(DECK,i) for i in inclus]
    # inclus = [plugs.Eve(DECK,bubase.dyna_a_include(p)) for p in fps]
 
    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()

    # duh = asb.chains_at_depth(1)
    duh = asb.chains()
    # print(duh)
  
    #-----------------------------------
    time.end() 
