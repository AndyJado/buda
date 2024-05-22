import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers



if __name__ == "__main__":
    os.system('clear')

    # M = ['a','b','o','p','q']
    # I = [('d',['h']), ('e',['i','j'])]
    # S = ['m','n']

    M = ['a','s']
    I = [('b',['c','d'])]
    S = ['h','e']

    all_possi = plugs.possi(M,I,S)

    print([str(i) for i in all_possi])
