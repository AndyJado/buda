from ansa import base, mesh,constants
from literals import Entities

# should also create set, bolt qulity requires another tuning
def openhole(deck:int,point:tuple[float,float,float], diameter:float):
    diameter = diameter + 1e-6
    props = base.CollectEntities(deck,None,Entities.PROPERTY)
    params_dict = {
        'zone_num': 0,
        'proj_tolerance': 102.0,
        'target_node_num': 8,
        'diameter': diameter,
        'zone1_len': 0.0,
        'zone2_len': 0.0,
        'quads_around_proj_point': True,
        'square_holes': False,
        'create_perfect_zone': True
    }

    params = tuple(params_dict.values())
    print(params)
    
    hole = (point, props, params)
    mesh.ProjectOpenHole((hole,))    

# refine elements to quad
def quad_remesh(props):
    shells = base.CollectEntities(constants.LSDYNA, props, "ELEMENT_SHELL", recursive=True)
    mesh.RefineElements(shells, 0, 1, 0.0, 1, 0, "QUAD", 0, 0)

