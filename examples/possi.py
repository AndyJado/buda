import ansa, itertools,os
import plugs,literals,bubase,buconnect,bumesh,bubase,buentity,helpers
from plugs import Possi

def possi(M:list,I:list[tuple[any,list]],S:list) -> list[Possi]:

    l_im = 0
    l_m = len(M)
    l_s = len(S)
    l_is = 0
    i_dict:dict[any,list] ={}

    for (s,ms) in I:
        l_is += 1
        l_im += len(ms)
        i_dict.update({s:ms})
    
    ms = list(i_dict.keys())

    empty1 = l_m - l_is
    empty2 = l_m + l_im - l_is - l_s

    assert empty2 >= 0 and empty1 >=0, "impossible!"

    for _ in range(0,empty1):
        ms.append(None)

    for _ in range(0,empty2):
        S.append(None)

    is_aranges = set(itertools.permutations(ms))
    s_aranges = set(itertools.permutations(S))

    # print('s_aranges:', s_aranges)

    pairs1:list[tuple[any,any]] = []

    for arange in is_aranges:
        pair = []
        for i,val in enumerate(arange):
            pair.append((M[i],val))
        pairs1.append(pair)

    # print('pairs1',pairs1)

    possi_assmbles = []

    for par in pairs1:
        possi_id= 0
        m_is_pair = [] 
        im = []
        im_s_pair = []
        for m,s in par:
            if s is None:
                im.append(m)
            else:
                m_is_pair.append((m,s))
                im.extend(i_dict[s])
        # print('im', im)
        for ang in s_aranges:
            one_im_s_pair = []
            for i,val in enumerate(im):
                one_im_s_pair.append((val,ang[i]))
            im_s_pair.append(one_im_s_pair)

        # print('M--iS', m_is_pair)
        # print('iM--S', im_s_pair)

        possi_assmbles.append(Possi(possi_id,m_is_pair,im_s_pair))
        possi_id += 1

    # print('one:', possi_assmbles[0])
    # print('lentgh:', len(possi_assmbles), len(possi_assmbles[0][1]))
    # print('permutation:',len(is_aranges),len(s_aranges))

    return possi_assmbles


if __name__ == "__main__":
    os.system('clear')

    # M = ['a','b','o','p','q']
    # I = [('d',['h']), ('e',['i','j'])]
    # S = ['m','n']

    M = ['a','s']
    I = [('b',['c','d'])]
    S = ['h','e']

    all_possi = possi(M,I,S)

    print([str(i) for i in all_possi])
