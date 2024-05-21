from enum import Enum
import math,itertools
import numpy as np
from typing import Callable, Iterable
from ansa import base,constants,calc
from literals import Entities
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
    
    class Ty(int,Enum):
        M = 0 # master
        I = 1 # intermidiate
        S = 2 # slave

    # def ms_append(self,)

## right hand rule for coordinate sys everywhere
## FIXME: now it simply parse a inclu
class Eve():

    cs_ty = Entities.COORD

    def __init__(self,deck:int,inclu:base.Entity) -> None:
        self.lyrs: list[Layer] = []

        CSs = base.CollectEntities(deck,inclu,self.cs_ty) #FIXME: there are other COORD lterals!
        assert len(CSs) >= 0, "no cs in include!"
        for cs in CSs:
            assert len(cs._name) > 0, "cs name empty!"
            dpth = self._parse_depth(cs._name)
            cur_lyr = self._cre_layer_if_none(dpth)
            # print(cur_lyr)
            peeled = self._remove_leading_parentheses(cs._name) 
            name_vec = peeled.split(' ')
            if name_vec[0] == 'S':
                cur_lyr.slave_cs(cs)
            elif name_vec[0] == 'M':
                cur_lyr.mcss.append(cs)
            else:
                print('coordinate system {} name should start with M or S !'.format(cs._name))
            # if cur_lyr.ty() == None:
            #     self.lyrs.pop()

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

        lyrs = [i for e in members for i in e.lyrs]

        for lyr in lyrs:
            d = lyr.depth
            if d not in self.layers:
                self.layers[d] = []
            cur = self.layers[d]
            cur.append(lyr)
    
    def __str__(self) -> str:
        return "{}".format([ "{}:{}".format(i,[l.__str__() for l in lyrs]) for (i,lyrs) in self.layers.items()])
    
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



# M = ['a','b'] # M
# MS = ['d','e'] # MS
# MM = ['h','i','j'] #MM should be determined by MS
# S = ['m','n'] # S
def possi(M:list,mS:list,mM:list,S:list):
    empty1 = len(M)-len(mS)
    empty2 = len(M) + len(mM) - len(mS) - len(S)

    assert empty2 >= 0 and empty1 >=0, "impossible!"

    for _ in range(0,empty1):
        mS.append(None)

    for _ in range(0,empty2):
        S.append(None)

    duh1 = set(itertools.permutations(mS))
    duh2 = set(itertools.permutations(S))


    res = []
    for i in duh1:
        for j in duh2:
            res.append([i,j])
            print([i,j],'\n\n')

    print(len(duh1),len(duh2))

