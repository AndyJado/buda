from ansa import base, mesh,constants
from literals import Entities,Meshes

# why the conformation check gui?
def openhole(deck:int,point:tuple[float,float,float], diameter:float,search_depth:float):
    diameter = diameter * 1.0 # must be a float
    search_depth *= 1.0
    props = base.CollectEntities(deck,None,Entities.PROPERTY)
    params_dict = {
        'zone_num': 1,
        'proj_tolerance': search_depth,
        'target_node_num': 8,
        'diameter': diameter,
        'zone1_len': 6.0,
        'zone2_len': 0.0,
        'quads_around_proj_point': False,
        'square_holes': False,
        'create_perfect_zone': True
    }

    params = tuple(params_dict.values())
    # print(params)
    
    hole = (point, props, params)
    mesh.ProjectOpenHole((hole,))    

# refine elements to quad
def quad_remesh(props):
    shells = base.CollectEntities(constants.LSDYNA, props, "ELEMENT_SHELL", recursive=True)
    mesh.RefineElements(shells, 0, 1, 0.0, 1, 0, "QUAD", 0, 0)

def ppt_ave_esize(ppt):
    eles = base.CollectEntities(0,ppt,Meshes.ELEMENT,True)
    return base.CalculateAverageMinMaxElementLength(eles)['average']

def nodes_from(ppt):
    return base.CollectEntities(0,ppt,Meshes.NODE,True)

def eles_from(ppt):
    return base.CollectEntities(0,ppt,Meshes.ELEMENT,True)

def dyna_ele_thickness_set(eles:list,t:float):
    cfg = {'THIC1':t,'THIC2':t,'THIC3':t,'THIC4':t,}
    for e in eles:
        e.set_entity_values(constants.LSDYNA,cfg)

