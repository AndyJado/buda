import glob,datetime
from typing import Iterable,List
from ansa import session,base,mesh,batchmesh,constants,calc,morph
import os,platform,time,logging,random
import literals,buconnect,bubase,plugs

class NewScript():

    def __init__(self,deck:int):

        if platform.system() == "Windows":
            os.system('cls')  # Windows命令清屏
        else:
            os.system('clear') 

        cwd = os.path.dirname(__file__)
        print('CWD:',cwd,'\n\n')

        self.start_time = time.time()
        os.chdir(cwd)
        session.New("discard")
        # close window not working
        base.SetCurrentDeck(deck)    

    def end(self):
        end_time = time.time()
        elapse_time = end_time - self.start_time
        print(f"ELAPSE TIME:{elapse_time} S\n")

# draw a rectangular at x-y-0
def draw_rec(width, length):
    node_x = (0, width, width, 0, 0)
    node_y = (0, 0, length, length, 0)
    curves = []
    for i in range(4):     
        p1 = [node_x[i], node_x[i+1]]
        p2 = [node_y[i], node_y[i+1]]
        p3 = [0, 0]
        curve_id = base.CreateCurve(2, p1, p2, p3)
        curves.append(curve_id)
        
    return curves

# draw circle at (0,0,0)
def draw_circle(deck:int,r:float) -> list[base.Entity]:
    origin=(0,0,0)
    p1=(1,0,0)
    p2=(0,1,0)
    curves = base.CreateCircleCenter2PointsRadius(origin,p1,p2,r)
    return [base.GetEntity(deck,literals.Entities.CURVE,id) for id in curves]
    # base.CurvesConnectMulti(curves='all')

def curve2plane(ents: list[base.Entity]) -> base.Entity:
    planes = base.FacesNewPlanar(ents,ret_ents=True)
    num = len(planes)
    assert num ==1, "these curve makes {} planes!".format(num)
    return planes[0]

# extrude a curve in Z
def extrude(curves, height):
    dir = []
    point1 = [0, 0, 0.]
    point2 = [0, 0, height]
    base.SurfaceExtrudeExtrude(select_entities=curves, dir_entities=dir, direction_method=0, internal_face=False, respect_user_selection=False, point1=point1, point2=point2)

# one property assurance!
def one_prop(deck:int, news = None,):
    news = news or {'Name':'default', 'T1': 3}
    prop_old = base.CollectEntities(deck, None, literals.Entities.PROPERTY)
    prop_new = base.CreateEntity(deck, literals.DynaCards.SHELL, news)
    for prop in prop_old:
        base.ReplaceProperty(prop, prop_new)
        
    base.DeleteEntity(prop_old, True)
    base.PidToPart()

def shell_mesh_local(deck:int,faceshell:base.Entity):
    mesh.SetMeshParamTargetLength("init_local", 1)
    mesh.Mesh(faceshell)

def shell_mesh_size(deck:int,shell:base.Entity,size:float):
    mesh.SetMeshParamTargetLength("absolute", size)
    mesh.Mesh(shell)

def a_plate_mesh(deck:int) -> base.Entity:
    curvs = draw_circle(deck,200)
    face = curve2plane(curvs)
    shell_mesh_local(deck,face)
    one_prop(deck,None)
    return base.GetEntity(deck,literals.Entities.PROPERTY,2) # idk but it's 2

def white_mouse_a_inclu(deck:int,curvs, cs_name: Iterable[str]):
    face = curve2plane(curvs)
    shell_mesh_local(deck,face)
    # one_prop(deck,None)
    # ppt = base.GetEntity(deck,literals.Entities.PROPERTY,2) # idk but it's 2
    ppts = base.CollectEntities(deck,face,literals.Meshes.ELEMENT)
    nodes = base.CollectEntities(deck,ppts,literals.Meshes.NODE,recursive=True) # must recursive

    inclu = random_cs_a_inclu(deck,set(nodes),cs_name)
    base.AddToInclude(inclu,ppts)
    return inclu

# return the INCLUDE
def random_cs_a_inclu(deck:int, nodes: Iterable[base.Entity],cs_name:Iterable[str]):
    f = lambda: (nodes.pop()._id for _ in range(3))
    css = []

    for name in cs_name:
        x,y,z = f()
        print('3 random nodes:',x,y,z)
        cys = buconnect.cre_coord_sys_3node(deck,x,y,z)
        while cys is None:
            x,y,z = f()
            cys = buconnect.cre_coord_sys_3node(deck,x,y,z)
        base.SetEntityCardValues(deck,cys,{'Name':name})
        css.append(cys)

    return bubase.ents_new_inclu(deck,css)

def random_move_ents(to_move:list[base.Entity],scale:int):
    rng = lambda: random.random() * scale

    base.GeoRotate('MOVE','AUTO_OFFSET',"SAME PART","NONE",rng(),rng(),rng(),rng(),rng(),rng(),rng(),to_move)

    base.GeoTranslate('MOVE','AUTO_OFFSET',"SAME PART","NONE",rng(),rng(),rng(),to_move)

def write_ents_with_ref(ents:list[base.Entity],path:str):
    base.OutputLSDyna(entities=ents,include_output_mode='references',filename=path)

def dir_a_asb(deck:int,dir:str):
    inclus = dir_to_inclus(dir)
    eves = [plugs.Eve(deck,i) for i in inclus]
    asb = plugs.Assemblr(deck,eves) 
    asb.possi_d_all()
    asb.chains_all()
    asb.elect_named()
    return asb

def dir_to_inclus(dir:str) -> list[base.Entity]:
    dir1 = os.path.join(dir,f'*.key')
    dir2 = os.path.join(dir,f'*.k')
    fps = glob.glob(dir1) + glob.glob(dir2)
    return [bubase.dyna_a_include(p) for p in fps]

# tested with inclu as ents
def cog(ents):
    info = base.DeckMassInfo('custom',ents,False)
    return info.cog,info.total_mass

class PropBox:
    def __init__(self, deck, ppts:List[base.Entity], coord:base.Entity):
        self.box = morph.MorphOrtho(loaded_elements = ppts, coordinate=coord)
        self.mopnts = morph.MorphCornerPoints(self.box)
        self.nodes = base.CollectEntities(deck, self.box, "MORPHPOINT", recursive=True)
        self.cnt = base.CollectEntities(deck, self.box, "MORPHCEPNT", recursive=True)
        self.cs = coord
        self.coord_id = coord._id
        # point Entity : local coordinates
        self.mdic = {}
        for pnts in self.mopnts:
            local = calc.GlobalToLocal(self.coord_id,pnts.position,'point')
            self.mdic.update({pnts:local})
    
    def morph_1d(self,direction:literals.Ax,distance:float):
        box_surf_pnts = [i[0] for i in sorted(self.mdic.items(),key=lambda x:x[1][direction])[:4]]
        x,y,z = direction.vec()
        param = morph.NewParameterTranslate(box_surf_pnts,x,y,z,self.cs)
        morph.MorphParam(param,distance)
    
    def measure(self):
        positions = [calc.GlobalToLocal(self.coord_id, node.position, "point") for node in self.nodes]

        mid_point_x = sum(x for x, _, _ in positions) / len(positions)
        mid_point_y = sum(y for _, y, _ in positions) / len(positions)
        mid_point_z = sum(z for _, _, z in positions) / len(positions)

        self.mid_point = (mid_point_x, mid_point_y, mid_point_z)

        xs, ys, zs = zip(*positions)
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)
        self.minz, self.maxz = min(zs), max(zs)

        self.length = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.width = self.maxz - self.minz        
        print(self.length,self.height,self.width)
        
    def delete(self):
        base.DeleteEntity(self.box,True)

def save_with_time(output_dir):
    current_time = datetime.datetime.now()
    folder_name = current_time.strftime("%m-%d_%H-%M")
    folder_path = os.path.join(output_dir, folder_name) 
    filename = os.path.join(folder_path,"run.key")

    if os.path.exists(folder_path):
        os.remove(filename)
        os.removedirs(folder_path)
        print('saving within minute interval! overwriting previous')

    os.makedirs(folder_path)
    bubase.output(filename)

def change_prop(old_prop:base.Entity,new_prop:base.Entity):
    base.ReplaceProperty(old_prop, new_prop)
    base.DeleteEntity(old_prop, False)
       
    return new_prop

def merge_props(target_prop:base.Entity,to_merge_props:List[base.Entity]):
    for p in to_merge_props:
        base.ReplaceProperty(p,target_prop)
        
    if target_prop in to_merge_props:
        to_merge_props.remove(target_prop)
        
    base.DeleteEntity(to_merge_props, True)
    return target_prop



def change_ele_pid(deck:int, nodes:List[base.Entity], pid):
    elements = base.NodesToElements(nodes)
    ele_selec_ids = set()
    for _, eles in elements.items():
        for ele in eles:
            ele_selec_ids.add(ele._id)

    for id in ele_selec_ids:           
        ent = base.GetEntity(deck,literals.Meshes.SHELL, id)
        ent.set_entity_values(deck, {'PID':pid}) #! id of property

