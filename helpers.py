from typing import Iterable
from ansa import session,base,mesh,batchmesh,constants
import os,platform,time,logging
import literals,buconnect,bubase

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

# draw circle at 
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

# extrude a curve
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
