import ansa,logging,sys,gc
import buconnect,bumesh,helpers,bubase,plugs

if __name__ == "__main__":
    DECK = ansa.constants.LSDYNA
    time = helpers.NewScript(DECK)
    #-----------------------------------

    # # d0
    # a = ['S','(M','((M']
    # b = ['S','M']
    # c = ['M']
    # #d1
    # d = ['(S']
    # #d2
    # e = ['((S']
    # pack = [a,b,c,d,e]

    pack = [['M','M'],['S','(S'],['M','S'],['(M']]

    inclus = [helpers.white_mouse_a_inclu(DECK,helpers.draw_rec(100,100),i) for i in pack]
    eves = [plugs.Eve(DECK,i) for i in inclus]

    asb = plugs.Assemblr(DECK,eves) 

    asb.possi_d_all()
    asb.chains_all()
    for chain in asb.chains:
        print(chain)


    #-----------------------------------
    time.end() 