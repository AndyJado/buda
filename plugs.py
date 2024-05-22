from enum import Enum
import math,itertools
import numpy as np
from typing import Callable, Iterable
from ansa import base,constants,calc
from literals import Entities
from ansa.base import Entity
import logging

def unplug_meshes(deck:int):
    nodes = base.CollectEntitiesI(deck,None,"NODE") # ELEMENT will delete parts!
    base.DeleteEntity(nodes,force=True)

def paramlater(deck:int, ent: base.Entity, field:str,name:str):
    cardic = ent.card_fields(deck,True)
    val = cardic.get(field) or  0 # 'None' if none
    param = base.CreateEntity(deck,"A_PARAMETER", {'Name':name})
    return ent.set_entity_values(deck,{field: '='+name})

class Layer():
    def __init__(self,d:int) -> None:
        self.depth = d
        self.scs: base.Entity = None
        self.mcss: list[base.Entity] = []
    
    def slave_cs(self,cs: base.Entity):
        assert self.scs is None, "scs is not None in this layer!"
        self.scs = cs
    
    def mas_cs(self,cs: base.Entity):
        self.mcss.append(cs)
    
    # FIXME: feels ugly
    def ty(self):
        if self.scs is None and len(self.mcss) == 0:
            return None

        if self.scs is None:
            return Layer.Ty.M
        elif len(self.mcss) == 0:
            return Layer.Ty.S
        else:
            return Layer.Ty.I
    
    def __str__(self):
        # res = 'depth:{}\nscs:{}\nmcss_:{}\n'.format(self.depth,self.scs,len(self.mcss))
        return str(self.ty())
    
    class Ty(str,Enum):
        M = 'M' # master
        I = 'I' # intermidiate
        S = 'S' # slave

    # def ms_append(self,)

# 
class Eve():

    cs_ty = Entities.COORD

    def __init__(self,deck:int,inclu:base.Entity) -> None:
        self.lyrs: dict[int,Layer] = {}
        self.inclu = inclu

        CSs = base.CollectEntities(deck,inclu,self.cs_ty) #FIXME: there are other COORD lterals!
        assert len(CSs) >= 0, "no cs in include!"
        for cs in CSs:
            assert len(cs._name) > 0, "cs name empty!"
            dpth = self._parse_depth(cs._name)
            if dpth not in self.lyrs:
                self.lyrs[dpth] = Layer(dpth)
            cur_lyr = self.lyrs[dpth]
            peeled = self._remove_leading_parentheses(cs._name) 
            name_vec = peeled.split(' ')
            if name_vec[0] == 'S':
                cur_lyr.slave_cs(cs)
            elif name_vec[0] == 'M':
                cur_lyr.mas_cs(cs)
            else:
                print('coordinate system {} name should start with M or S !'.format(cs._name))
    
    def __str__(self) -> str:
        return "{}".format([l.__str__() for l in self.lyrs])
    
    def _remove_leading_parentheses(self,s):
        while s and s[0] == '(':
            s = s[1:]
        return s

    def _cre_layer_if_none(self,d:int):
        lyrs = [l for l in self.lyrs if l.depth == d]
        if len(lyrs) == 0:
            lyr = Layer(d)
            self.lyrs.append(lyr)
            return self.lyrs[0]
        elif len(lyrs) == 1:
            return self.lyrs[0]
        else:
            print('ERROR')
            assert "1 depth 1 Layer!"
    
    def _parse_depth(self, s: str)-> int:
        count = 0
        for char in s:
            if char == '(':
                count += 1
            else:
                break
        return count


    
## FIXME: to test possibles !==1
class Assemblr():

    def __init__(self,deck:int,members:Iterable[Eve]) -> None:

        self.CHAINS:list[list[base.Entity]] = []
        # {depth : [layer]}
        self.layers: dict[int,list[Layer]] = {}
        self.deck = deck

        for e in members:
            for (d,lyr) in e.lyrs.items():
                if d not in self.layers:
                    self.layers[d] = []
                cur = self.layers[d]
                cur.append(lyr)
    
    def __str__(self) -> str:
        return "{}".format([ "{}:{}".format(i,[l.__str__() for l in lyrs]) for (i,lyrs) in self.layers.items()])
    
    def mis_id_at_depth(self,d:int):
        css = self.layers[d] #FIXME: if no key?
        M = [css._id for l in css if l.ty() == 'M' for css in l.mcss]
        I = [(l.scs,l.mcss) for l in css if l.ty() == 'I']
        S = [l.scs._id for l in css if l.ty() == 'S']
        Iids = []
        for s,ms in I:
            Iids.append((s._id,[cs._id for cs in ms]))
        return M,Iids,S

    def assemble_layer(self,d:int):
        M,I,S = self.mis_id_at_depth(d)
        layer_possis = possi(M,I,S)
        for p in layer_possis:
            pass


    def recurr(self):
        cur_depth = min(self.layers.keys())
        cur = self.layers[cur_depth]
        return [ly.ty() for ly in cur]
       
    def final(self):

        possi = len(self.CHAINS) 

        assert possi == 1, "CANNOT FINAL! {} possibles remains!".format(self.CHAINS)

        css_stack = self.CHAINS[0]

        inclus = [base.GetEntityInclude(cs) for cs in css_stack]

        ppts = [ppt for icl in inclus for ppt in base.CollectEntities(self.deck,icl,Entities.PROPERTY)]

        # ppts = [ppt for icl in inclus for ppt in base.CollectEntities(self.deck,icl,[Entities.PROPERTY,Entities.COORD])] #FIXME: move COORD


        to_tran = []

        while css_stack:
            to_tran.append(ppts.pop())
            align_by_matrix(self.deck,to_tran,css_stack.pop(),css_stack.pop())
   
    def mm_from_ms(ms:base.Entity):
        inclu = base.GetEntityInclude(ms)
        base.CollectEntities()


def array_matrix(deck, coord:base.Entity):
    matrix = calc.GetCoordTransformMatrix4x3(deck, coord, 0,0,0)
    matrix = np.array(matrix)
    matrix = matrix.T
    new_row = np.array([[0, 0, 0, 1]])
    matrix = np.vstack([matrix, new_row])
    
    return matrix
    
        
def trans_matrix_from_2_coords(deck, slave_coord:base.Entity, master_coord:base.Entity):
    matrix_S = array_matrix(deck, slave_coord)
    matrix_S = np.linalg.inv(matrix_S)

    matrix_M = array_matrix(deck, master_coord)
    
    trans_matrix = np.dot(matrix_M, matrix_S)
    trans_matrix = np.delete(trans_matrix, -1, axis=0)
    trans_matrix = trans_matrix.T
    
    return trans_matrix
    
    
def align_by_matrix(deck, slave_ent:list[base.Entity], slave_coord:base.Entity, master_coord:base.Entity):
    trans_matrix = trans_matrix_from_2_coords(deck, slave_coord, master_coord)
    base.TransformMatrix4x3(
        input_function_type="MOVE",
        pid_offset="AUTO_OFFSET",
        group_offset="NEW PART",
        input_sets_type="EXPAND",
        matrix=trans_matrix,
        entities=slave_ent,
        draw_results=True,
        keep_connectivity=True,
    )

# BUG: kill !
class Possi():

    def __init__(self,id:int,lhs:list,rhs:list) -> None:
        self.id = id
        self.lhs = lhs
        self.rhs = rhs
    
    def __str__(self) -> str:
        return "MASTER:{},SLAVE_POSSIBLES:{}".format(self.lhs,len(self.rhs))

def possi(M:list,I:list[tuple[any,list]],S:list):

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
