from ansa import connections,base,calc,constants
from literals import Entities,Meshes,DynaCards

# FIXME: to test 
class BoltBuilder():

    BOLT_CFG: dict=None

    # FIXME: must have holes at this point
    def __init__(self,deck:int) -> None:
        self.deck = deck
        globe = base.CollectEntities(deck,None,DynaCards.SHELL)
        self.cnctns:list[base.Entity] = connections.DefineConnectionHoles(
            entities=globe,
            create="Bolt_Type",
            output_mode="properties",
            search_holes=True,
            use_hole_shape=True,
            hole_minimum_diameter=0.0,
            hole_maximum_diameter=50.0,
            parts_proximity_for_connection_merging=100,
            match_hole_params='any'
        )
        cns = len(self.cnctns)
        assert cns >= 1, "there is {cns} holes!".format(cns)
    
    def solid_bolt(self,d:float,len:float):
        self.BOLT_CFG = {
        "FE Rep Type": "SOLID BOLT",  
        "Length": len,  
        "D": d, 
        "Search Dist": 100,
        "Search From": -100,
        "Search To": 100,
        "Search For Holes": "yes",
        "Respect PID Thickness": "yes",
        "Bolt Length": 1.8,
        "Head Diameter": 1.5,
        "Head Diameter Mult": "*Diam",
        "Head Height": 10,
        "Create Nut": "yes",
        "Pasted to Thread": "no",
        # "Create Pretension": "yes",
        # "Pretension Representation": "LS-DYNA: Load Curve",
        # "LCID": curve_id,
        }
    
    def apply(self):
        [cnct.set_entity_values(self.deck,self.BOLT_CFG,debug=constants.REPORT_ALL) for cnct in self.cnctns]
        connections.ReApplyConnections(self.cnctns)

#! FIXME: works only with dyna! get nd position!
def dp(nid:int)->tuple[float,float,float]:
    nd = base.GetEntity(constants.LSDYNA,Meshes.NODE,nid)
    return nd.position

#! FIXME: create coord sys from 3 node 
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

def local_translate(type:str,cid:int,vec:list[float,float,float],ents:list[base.Entity]):
    x,y,z= calc.LocalToGlobal(cid,vec,'vector')
    base.GeoTranslate(
    type,
    'AUTO_OFFSET',
    "SAME PART",
    "NONE",
    x,
    y,
    z,
    ents,
    keep_connectivity=True,
    draw_results=False,
    )