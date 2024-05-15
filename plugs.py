import math
import numpy as np
from typing import Callable
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


## right hand rule for coordinate sys everywhere
##
class Eve():
    def __init__(self,deck:int,inclu:base.Entity) -> None:
        ## coordinate systems 
        mcss: list[base.Entity] = []
        scs: base.Entity = None
        CSs = base.CollectEntities(deck,inclu,Entities.COORD,recursive=True)
        assert len(CSs) != 0, "no cs in include!"
        for cs in CSs:
            assert len(cs._name) > 0, "cs name empty!"
            name_vec = cs._name.split(' ')
            if name_vec[0] == 'S':
                scs = cs
            elif name_vec[0] == 'M':
                mcss.append(cs)
            else:
                print('coordinate system {} name should start with M or S !'.format(cs._name))
       
        self.scs,self.mcss = scs, mcss
    
## FIXME: to test possibles !==1
class Assemblr():

    CHAINS:list[list[base.Entity]] = []

    def __init__(self,deck:int,members:Iterable[Eve]) -> None:
 
        self.deck = deck
        masters:list[base.Entity] = []
        mid_m:list[base.Entity] = []
        mid_s:list[base.Entity] = []
        slaves:list[base.Entity] = []
        
        for ev in members:
            if ev.scs is None:
                for cs in ev.mcss:
                    masters.append(cs)
            elif len(ev.mcss) == 0:
                slaves.append(ev.scs)
            else:
                mid_m.extend(ev.mcss)
                mid_s.append(ev.scs)

        self.M = masters
        self.MM = mid_m
        self.MS = mid_s
        self.S = slaves

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
   
    ## l1,l2 -- r1,r2
    def possibles(self) -> int:
        m = len(self.M)
        mm = len(self.MM)
        ms = len(self.MS)
        s = len(self.S)

        if mm == ms == 0 and m == s == 1:
            self.CHAINS=[[self.M[0],self.S[0]]]
            return 1

        if m == mm == ms == s == 1:
            self.CHAINS=[[self.M[0],self.MS[0],self.MM[0],self.S[0]]]
            return 1
        
        l1_remain = m - mm
        assert l1_remain >= 0, "{}<{}".format(m,mm)
        r1 = ms + l1_remain      
        assert r1 == s, "{}!={}".format(r1,s)

        return _permutations(l1_remain,l1_remain)*_permutations(s,s)

        
# 计算排列数 P(n, k)
def _permutations(n, k):
    return math.factorial(n) // math.factorial(n - k)

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



