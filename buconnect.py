from typing import Tuple
from ansa import connections,base,calc,constants
from literals import Entities,Meshes,DynaCards,Constrains
import bubase

class BoltBuilder():

    # FIXME: must have holes at this point
    def __init__(self,deck:int,diameter_uuid:float=None) -> None:
        self.deck = deck
        self.BOLT_CFG: dict = None

        # print('bolt had',had_ids)
        if diameter_uuid is None:
            d_min= 0.0
            d_max = 50.0
        else:
            d_min = diameter_uuid - 1e-5
            d_max = diameter_uuid + 1e-5

        globe = base.CollectEntities(deck,None,Entities.PROPERTY) #FIXME: searching holes scope here
        cncts_all:list[base.Entity] = connections.DefineConnectionHoles(
            entities=globe,
            create="Bolt_Type",
            output_mode="properties",
            search_holes=True,
            use_hole_shape=True,
            hole_minimum_diameter=d_min,
            hole_maximum_diameter=d_max,
            hole_proximity_angle=30,
            parts_proximity_for_connection_merging=100,
            match_hole_params='any',
        )

        self.cnctns:list[base.Entity] = cncts_all

        cns = len(self.cnctns)
        assert cns >= 1, "there is {} hole!,dmax: {},dmin:{}".format(cns,d_max,d_min)
    
    def solid_bolt(self,d:float,len:float,curve_id:int):
        self.BOLT_CFG = {
        "FE Rep Type": "SOLID BOLT",  
        "Length": len,  
        "D": d, 
        "Search Dist": 300,
        "Search From": -150,
        "Search To": 150,
        "Search For Holes": "yes",
        "Respect PID Thickness": "yes",
        "Bolt Length": 1.8,
        "Head Diameter": 1.5,
        "Head Diameter Mult": "*Diam",
        "Head Height": 10,
        "Head Num of Rows": 1,
        "Create Nut": "yes",
        "Create Washer": "yes",
        "Create Nut Washer": "yes",
        "Washer Num of Rows": 1,
        "Washer Outer Diameter": 2.5,
        "Washer Num of Nodes": 12,
        "Pasted to Thread": "yes",
        "Mesh Pattern": "4-quad octagon",
        "Thread Num of Rows":int(len/5),
        "Create Pretension": "yes",
        "Pretension Representation": "LS-DYNA: Load Curve",
        "LCID": curve_id,
        }
    
    def apply(self):
        [cnct.set_entity_values(self.deck,self.BOLT_CFG) for cnct in self.cnctns]
        connections.ReApplyConnections(self.cnctns)
    

#! FIXME: works only with dyna! get nd position!
def dp(nid:int)->tuple[float,float,float]:
    nd = base.GetEntity(constants.LSDYNA,Meshes.NODE,nid)
    return nd.position

#!create coord sys from 3 node 
def cre_coord_sys_3node(deck:int,nid_o:int,nid_x:int,nid_y:int) -> base.Entity:
    coord_orig = dp(nid_o)
    coord_x = dp(nid_x)
    coord_y = dp(nid_y)

    fields = {
        'DEFINITION METHOD': 'DEFAULT METHOD',
        'XO': coord_orig[0],
        'YO': coord_orig[1],
        'ZO': coord_orig[2],
        'XL': coord_x[0],
        'YL': coord_x[1],
        'ZL': coord_x[2],
        'XP': coord_y[0],
        'YP': coord_y[1],
        'ZP': coord_y[2],
    }
    
    return base.CreateEntity(deck, Entities.COORD, fields)

def copy_along_cs(cid:int,vec:list[float,float,float],ents:list[base.Entity]):
    x,y,z= calc.LocalToGlobal(cid,vec,'vector')
    base.GeoTranslate(
    'COPY',
    'AUTO_OFFSET',
    "SAME PART", # same ansa group
    "EXPAND", # set will simply move with
    x,
    y,
    z,
    ents,
    )

def rotate_along_cs(cid:int,angle:float,axis:tuple,ents):
    x0,y0,z0 = calc.LocalToGlobal(cid,[0,0,0],'point')
    x,y,z = calc.LocalToGlobal(cid,axis,'point')
    base.GeoRotate('MOVE','AUTO_OFFSET','SAME PART','NONE',x0,y0,z0,x,y,z,angle,ents)

def move_along_cs(cid:int,vec:list[float,float,float],ents:list[base.Entity]):
    x,y,z= calc.LocalToGlobal(cid,vec,'vector')
    base.GeoTranslate(
    'MOVE',
    'AUTO_OFFSET',
    "SAME PART",
    "NONE", # set will simply move with
    x,
    y,
    z,
    ents,
    )

# ppt should be ansa property
def ppt_dependent_ppts(deck:int,ppt:base.Entity):
    nds = base.CollectEntities(deck,ppt,Meshes.NODE,recursive=True)
    
    assert len(nds)>0, "{}".format(nds)

    return bubase.nodes2ppts(deck,nds)

def miror_ents_cs( deck:int,ents:list[base.Entity],cid:int,vec1:Tuple[float,3],vec2:Tuple[float,3]):
    x0,y0,z0 = calc.LocalToGlobal(cid,[0,0,0],'point')
    x1,y1,z1 = calc.LocalToGlobal(cid,vec1,'point')
    x2,y2,z2 = calc.LocalToGlobal(cid,vec2,'point')
    base.GeoMirrorPlane("COPY",0,"SAME PART","EXPAND",x0,y0,z0,x1,y1,z1,x2,y2,z2,ents,True,True)


def miror_ents_3_nodes(deck:int,ents:list[base.Entity],ref_nodes:Tuple[int,3]):
    nd_posis = [pos for i in ref_nodes for pos in base.GetEntity(deck,Meshes.NODE,i).position]
    nd_posis.reverse()
    p = lambda: nd_posis.pop()
    base.GeoMirrorPlane("COPY",0,"SAME PART","EXPAND",p(),p(),p(),p(),p(),p(),p(),p(),p(),ents,True,True)

#FIXME: more or less useless, 
def get_revolute_joint_rigid_pair(deck:int,jid:int)->tuple[base.Entity,base.Entity]:
    kwd='CONSTRAINED_JOINT_REVOLUTE'
    joint = base.GetEntity(deck,kwd,jid)
    # print(joint.card_fields(deck))

    nds = joint.get_entity_values(deck,['N1','N2'])

    nd1 = nds['N1']
    nd2 = nds['N2']

    print(nd1)

    return(_get_ppt_from_extra_nodes(deck,nd1),_get_ppt_from_extra_nodes(deck,nd2))

def _get_ppt_from_extra_nodes(deck:int,node:base.Entity):
    nd1_refs:list[base.Entity] = base.ReferenceEntities(node)

    extras = [ent for ent in nd1_refs if ent.ansa_type(deck) == Constrains.EXTRA_NODE]

    pidic = extras[0].get_entity_values(deck,['PID'])

    return pidic['PID']


# rigid node id
def get_rigid_node_ppts(deck:int, rnid:int)->list[base.Entity]:
    kwd='CONSTRAINED_NODAL_RIGID_BODY'

    rigid_nd = base.GetEntity(deck,kwd,rnid)
    print(rigid_nd.card_fields(deck))

    nset = rigid_nd.get_entity_values(deck,['NSID']) #FIXME: always use set?

    nset:base.Entity = nset['NSID']
    # print('nset fields', nset.card_fields(deck,True))

    # nodes
    inset = base.CollectEntities(deck,nset,None)
    # print('nset', inset)
    return bubase.nodes2ppts(deck,inset)
    
def point2local(cid:int,coord:tuple):
    return calc.GlobalToLocal(cid,coord,'point')    

def point2global(cid:int,coord:tuple):
    return calc.LocalToGlobal(cid,coord,'point')