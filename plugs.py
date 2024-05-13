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
    def __init__(self,deck:int,path:str) -> None:
        self.deck = deck
        inclu = base.InputLSDyna(path,header='overwrite',new_include='on',create_parameters='on')
        
        self.INCLU = inclu
        ## coordinate systems 
        self.scs,self.mcss = self._parse_css_name()

        self.SETS = self._get(Entities.SET)
        self.PART = self._get(Entities.PROPERTY)
    
    def _get(self,ty:str):
        return base.CollectEntities(self.deck,self.INCLU,ty)
    
    # parse INCLUDE, return master and slave cs
    def _parse_css_name(self):
        mcss: list[base.Entity] = []
        scs: base.Entity = None
        CSs = self._get(Entities.COORD)
        # return [cs._name for cs in CSs]
        for cs in CSs:
            assert len(cs._name) > 0, "cs name empty!"
            name_vec = cs._name.split(' ')
            if name_vec[0] == 'S':
                scs = cs
            elif name_vec[0] == 'M':
                mcss.append(cs)
            else:
                print('{} is unregulated cs!'.format(cs._name))
        
        return scs,mcss

class Assemblr():

    CHAINS:list[list[base.Entity]] = []


    def __init__(self,deck:int,members:list[Eve]) -> None:
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
        possi = self._possibles()
        assert possi ==1, "not final,{} possibles remain".format(possi)

        css_stack = self.CHAINS[0]

        inclus = [base.GetEntityInclude(cs) for cs in css_stack]

        ppts = [ppt for icl in inclus for ppt in base.CollectEntities(self.deck,icl,Entities.PROPERTY)]

        to_tran = []

        while css_stack:
            to_tran.append(ppts.pop())
            align_by_matrix(self.deck,to_tran,css_stack.pop(),css_stack.pop())
   
    ## l1,l2 -- r1,r2
    def _possibles(self) -> int:
        m = len(self.M)
        mm = len(self.MM)
        ms = len(self.MS)
        s = len(self.S)

        if m == mm == ms == s == 1:
            self.CHAINS.append([self.M[0],self.MS[0],self.MM[0],self.S[0]])
            return 1

        l1 = m - mm
        assert l1 >= 0, "{}<{}".format(m,mm)
        r1 = ms + l1      
        assert r1 == s, "{}!={}".format(r1,s)

        return _permutations(l1,l1)*_permutations(s,s)

        

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



