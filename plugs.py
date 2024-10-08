from enum import Enum
import math,itertools,os,time
import numpy as np
from typing import Callable, Iterable, List, Tuple,TypeVar
from ansa import base,constants,calc,guitk
from literals import Entities,Meshes
from ansa.base import Entity
import logging
from collections import Counter

A = TypeVar('A')

def unplug_meshes(deck:int):
    nodes = base.CollectEntitiesI(deck,None,"NODE") # ELEMENT will delete parts!
    base.DeleteEntity(nodes,force=True)

Pair = Tuple[A,A]
Chain = List[Pair]

class Possi():

    def __init__(self,id:int,lhs:list[Pair],rhs:list[list[Pair]]) -> None:
        self.id = id
        self.lhs = lhs
        self.rhs = rhs
    
    # each chain denotes expresses a possi
    def chains(self):
        if len(self.lhs) == 0:
            return self.rhs
        if len(self.rhs) == 0:
            return [self.lhs]
        return [self.lhs + rprs for rprs in self.rhs]
    
    def _no_way(self):
        self.lhs = []
        self.rhs = []

    def arrest_pair(self,criminal:Pair):
        if criminal in self.lhs:
            self._no_way()
        
        self.rhs = [pars for pars in self.rhs if criminal not in pars]
                

    def possi_check(self)->int:

        lsp = len(self.rhs) # left salve possibles?
        if lsp == 0:
            return 1
        return lsp
    
    def __str__(self) -> str:
        return "MASTER:{},SLAVES:{}".format(self.lhs,self.rhs)

# Eve has depth layer
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

    #FIXME: there are others ty of COORD
    cs_ty = Entities.COORD

    def __init__(self,deck:int,inclu:base.Entity) -> None:
        self.lyrs: dict[int,Layer] = {}
        self.inclu = inclu
        self.cs_names : dict[int,str] = {}

        CSs = base.CollectEntities(deck,inclu,self.cs_ty) #FIXME: there are other COORD lterals!
        assert len(CSs) >= 0, "no cs in include!"
        for cs in CSs:
            assert len(cs._name) > 0, "cs id: {} name empty!".format(cs._id)

            dpth = self._parse_depth(cs._name)
            if dpth not in self.lyrs:
                self.lyrs[dpth] = Layer(dpth)
            cur_lyr = self.lyrs[dpth]
            peeled = self._remove_leading_parentheses(cs._name) 
            name_vec = peeled.split(' ')
            name_vec.reverse()
            cs_ty = name_vec.pop()
            if cs_ty == 'S':
                assert cur_lyr.scs is None,"{}breaking slave cs owenership rule!".format(self)
                cur_lyr.slave_cs(cs)
            elif cs_ty == 'M':
                cur_lyr.mas_cs(cs)
            elif cs._name.startswith('^'):
                new_cs_name = cs._name.removeprefix('^')
                cs.set_entity_values(deck,{'Name':new_cs_name})
            else:
                print('coordinate system {} name should start with M or S !'.format(cs._id))

            name_vec.reverse()
            if len(name_vec) > 0:
                name = name_vec.pop()
                self.cs_names.update({cs._id:name})
    
    def _get(self,deck:int,ty:str):
        ents = base.CollectEntities(deck,self.inclu,ty)
        if len(ents) == 1:
            return ents[0]
        else:
            print('{} {} in {}'.format(len(ents),ty,self.inclu._name))# FIXME: don't do this
            return ents

    def _2set(self,deck:int):
        prop = base.CollectEntities(deck,self.inclu,Entities.PROPERTY)
        filename = self.inclu._name
        name = filename.split('.')[0]
        set = base.CreateEntity(deck,Entities.SET,{'Name':'props_{}'.format(name)})# FIXME: naming tricks caution
        base.AddToSet(set,prop)
        return set

    def _add(self,ent:base.Entity):
        base.AddToInclude(self.inclu,ent)

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

# a 3 recur unit consists of M and I and S
MIS = Tuple[List[A],List[Tuple[A,List[A]]],List[A]]
    
class Assemblr():

    def __init__(self,deck:int,members:Iterable[Eve]) -> None:

        # {depth : [layer]}
        self.layers: dict[int,MIS] = {}
        # for election
        self.named_cs: dict[int,str] = {}
        # suck all eve 
        self.inclus: list[Entity] = []
        # {depth: [possi]}
        self.dps: dict[int,list[Possi]] ={}
        self.deck = deck
        # possibles[layers[paris]]
        self.chains: Iterable[Iterable[Iterable[Pair]]] = []

        for e in members:
            self.cs_ty = e.cs_ty
            self.inclus.append(e.inclu)
            self.named_cs.update(e.cs_names)
            for (d,lyr) in e.lyrs.items():

                if d not in self.layers:
                    self.layers[d] = ([],[],[])

                cur = self.layers[d]

                if lyr.ty() == 'M':
                    mids = [i._id for i in lyr.mcss]
                    cur[0].extend(mids)

                if lyr.ty() == 'I':
                    iids = (lyr.scs._id,[cs._id for cs in lyr.mcss])
                    cur[1].append(iids)

                if lyr.ty() == 'S':
                    sid = lyr.scs._id
                    cur[2].append(sid)

                # e.inclu.set_entity_values(self.deck,{'Name':lyr.ty()})
    
    def __str__(self) -> str:
        return "{}".format([ "{}:{}".format(i,[l.__str__() for l in lyrs]) for (i,lyrs) in self.layers.items()])

    def possibles_each_depth(self):
        left = {}
        for k,val in self.dps.items():
            left[k] = len(val)
        print('left has',left)
        return left
    
    def pairs_all(self):
        res:list[Pair] = []
        for ps in self.dps.values():
            for p in ps:
                [ res.append(pr) for chain in p.chains() for pr in chain]
        return res
    
    def pair_counter(self):
        flatten_pairs = [pr for chain in self.chains for prs in chain for pr in prs]
        count = Counter(flatten_pairs)
        return count
    
    def cs_counter(self):
        pair_counter = self.pair_counter()
        leasts = [i[0] for i in sorted(pair_counter.items(), key=lambda item: item[1])] 
        flatten:list[int] = [csid for pr in leasts for csid in pr]
        return Counter(flatten)

    # only master can name slave
    def elect_named(self):
        all_pairs = self.pairs_all()

        for id,name in self.named_cs.items():
            candi = []
            for mid,sid in all_pairs:
                if sid is not None:
                    if mid == id:
                        candi.append(sid)
       
            for sid in candi:
                cs_ent = base.GetEntity(self.deck,Entities.COORD,sid)
                icl = base.GetEntityInclude(cs_ent)
                # icl.card_fields(self.deck,True)
                base_name = os.path.splitext(icl._name)[0]
                if base_name == name:
                    print('electing named pairs:{}'.format(base_name))
                    self.elect_pair(id,sid)

    def elect_pair(self,csid:int,csid2:int):
        pair = ((csid,csid2),(csid2,csid))
        self.chains = [ps for candi in pair for ps in self.chains for pars in ps if candi in pars]

    def arrest_pair(self,csid:int,csid2:int):
        pair = ((csid,csid2),(csid2,csid))
        [p.arrest_pair(criminal) for criminal in pair for ps in self.dps.values() for p in ps]

    # update all possibles in all depth to self.dps
    def possi_d_all(self):
        for k in self.layers.keys():
            self.possi(k)
    
    def possi(self,d:int):
        assert self.dps.get(d) is None, "possi already there!"

        M,I,S = self.layers[d]

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

        #FIXME
        assert empty2 >= 0 and empty1 >=0, "ERROR: free slaves are not supported yet!\nIf allows, there would be floating parts in the final asb,maybe after layer inference\nFREE Intermidate:{},FREE Slave:{}\nasb:{}\nimpossible at depth{}".format(empty1,empty2,self,d)

        for _ in range(0,empty1):
            ms.append(None)

        for _ in range(0,empty2):
            S.append(None)

        is_aranges = set(itertools.permutations(ms))
        s_aranges = set(itertools.permutations(S))

        print('Assembly depth {} has: {} x {} possibles '.format(d, len(is_aranges) , len(s_aranges)))

        pairs1:list[tuple[any,any]] = []

        for arange in is_aranges:
            pair = []
            for i,val in enumerate(arange):
                pair.append((M[i],val))
            pairs1.append(pair)

        # print('pairs1',pairs1)

        possi_assmbles:list[Possi] = []

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

        self.dps.update({d:possi_assmbles}) 
    
    def chains_all(self):
        keys = list(self.dps.keys())
        keys.sort()
        lists = [self.chains_at_depth(d) for d in keys]
        # self.chains = list(itertools.product(*lists))
        res = itertools.product(*lists)
        for i in res:
            self.chains.append(i)
               
            
    def chains_at_depth(self,d:int):
        ps = self.dps[d]
        return [chain for p in ps for chain in p.chains()]

    def try_final(self):

        if len(self.chains) != 1:
            print("assemble has {} possibles".format(len(self.chains)))
            return

        print('**----1 possible remians, finaling ASSEMBLY----**') 
        self.realize_chain_id(0)
        print('\nSUCCESS, ASSEMBLE FINISHED \n')

    def realize_chain_id(self,idx:int):
        depth  = 0
        for pars in self.chains[idx]:
            nog = "At depth {}, assembling coordinate piar {}".format(depth,pars)
            print(nog)
            depth += 1
            for par in pars:
                self.realize_pair(par)
    
    def realize_pair(self,pair:Pair):
        mcsid,scsid = pair
        if scsid is None: return
        self.transform_inclu(mcsid,scsid)
    
    def transform_inclu(self,mcsid:int,scsid:int):
        mcs = base.GetEntity(self.deck,self.cs_ty,mcsid)
        scs = base.GetEntity(self.deck,self.cs_ty,scsid)
        slave_inclu = base.GetEntityInclude(scs)
        master_inclu = base.GetEntityInclude(mcs)

        to_tran_ents_ty = [Entities.PROPERTY,Entities.COORD,Meshes.ELEMENT,Meshes.NODE,Entities.MATERIAL,Entities.SET,Entities.CONNECT,"INITIAL_STRESS_SECTION"]

        # to_tran_ents_ty = [Entities.ALL] #! BUG

        to_tran_slave = base.CollectEntities(self.deck,slave_inclu,to_tran_ents_ty)

        align_by_matrix(self.deck,to_tran_slave,scs,mcs)

        base.DeleteEntity([mcs,scs])

        ents_in_slave = base.CollectEntitiesI(self.deck,slave_inclu,to_tran_ents_ty)

        base.AddToInclude(master_inclu,ents_in_slave)

    def buttn(self):
        
        bak = base.CollectEntities(self.deck,self.inclus,Entities.ALL)
        
        def pop(action,data):
            model = base.GetCurrentAnsaModel()
            base.DestroyAnsaModel(model)
            self.chains.pop()
            remain = len(self.chains)
            print('POPING!, left:',remain)
            return 0
            
        def next(action, data):
            print('nexting')
            orig = base.GetCurrentAnsaModel()
            model = base.CreateNewAnsaModel()
            base.CopyEntitiesToAnsaModel(model,bak)
            base.SetCurrentAnsaModel(model)
            base.Not(orig)
            next = self.chains[-1]
            for dps in next:
                for par in dps:
                    self.realize_pair(par)
            print('next_done')
            return 0
        

        window = guitk.BCWindowCreate("Action", guitk.constants.BCOnExitDestroy)

        action = guitk.BCActionCreate(window, "pop", pop)

        action_salve = guitk.BCActionCreate(window,"next",next)

        next_lhs = guitk.BCPushButtonCreate(window, "pop", None, None)

        next_rhs = guitk.BCPushButtonCreate(window, "next", None, None)


        # this line make button trigger action
        guitk.BCActionAddWidget(action, next_lhs)
        guitk.BCActionAddWidget(action_salve,next_rhs)

        guitk.BCShow(window)





       
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

# AI code
def generate_combinations(arrays, current_index=0, current_combination=[]):
    if current_index == len(arrays):
        return [current_combination]
    combinations = []
    for value in arrays[current_index]:
        new_combination = current_combination + [value]
        combinations.extend(generate_combinations(arrays, current_index + 1, new_combination))
    return combinations
