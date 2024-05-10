from ansa import base, mesh
from . import buentity

# should also create set, bolt qulity requires another tuning
def openhole(deck:int,point:tuple[float,float,float], diameter:float):
    point = point
    props = base.CollectEntitiesI(deck,None,buentity.GenEnts.PROPERTY)
    params_dict = {
        'zone_num': 0,
        'proj_tolerance': 12.0,
        'target_node_num': 8,
        'diameter': diameter,
        'zone1_len': 0.0,
        'zone2_len': 0.0,
        'quads_around_proj_point': True,
        'square_holes': False,
        'create_perfect_zone': False
    }
    params = tuple(params_dict.values())
    print(params)
    
    hole = (point, props, params)
    mesh.ProjectOpenHole((hole,),'new_hole',True,True)    

