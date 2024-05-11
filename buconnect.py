from ansa import connections,base,calc,constants
from literals import Entities,Meshes,DynaCards

# FIXME: to test 
class BoltBuilder():

    BOLT_CFG: dict=None

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
    
    def solid_bolt(self,d:float,len:float):
        self.BOLT_CFG = {
        "FE Rep Type": "SOLID BOLT",    # bolt type
        "Length": len,    # length of bolt
        "D": d,   # diameter of bolt
        
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
        print(self.BOLT_CFG)
        [cnct.set_entity_values(self.deck,self.BOLT_CFG,debug=constants.REPORT_ALL) for cnct in self.cnctns]
        print(self.cnctns[0].card_fields(self.deck,True))
        connections.ReApplyConnections(self.cnctns)

#! FIXME: works only with dyna
def dp(nid:int)->tuple[float,float,float]:
    nd = base.GetEntity(constants.LSDYNA,Meshes.NODE,nid)
    return nd.position

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

def local_translate(type:str,cid:int,dx,dy,dz,ents:list[base.Entity]):
    x,y,z= calc.LocalToGlobal(cid,[dx,dy,dz],'vector')
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