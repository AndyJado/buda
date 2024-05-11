from ansa import session,base,mesh,batchmesh,constants
import os,platform,time
import literals

DECK= constants.LSDYNA

class NewScript():

    def __init__(self,deck:int):

        if platform.system() == "Windows":
            os.system('cls')  # Windows命令清屏
        else:
            os.system('clear') 

        self.start_time = time.time()
        print('STARTING AT TIME:',self.start_time,'\n\n')

        cwd = os.path.dirname(__file__)
        print('CWD:',cwd,'\n\n')
        os.chdir(cwd)
        session.New("discard")
        base.SetCurrentDeck(deck)    

    def end(self):
        end_time = time.time()
        elapse_time = end_time - self.start_time
        print(f"ELAPSE TIME:{elapse_time} S\n")

# draw a rectangular
def cre_quad(width, length):
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

def shell_mesh(deck:int,parts, target_element_length):
    parts = parts or base.CollectEntities(deck, None, "SECTION_SHELL")
    mesh.SetMeshParamTargetLength("absolute", target_element_length)

    session = batchmesh.GetNewSession("new")
    for part in parts:
        batchmesh.AddPartToSession(part, session)
        batchmesh.RunSession(session)
    

    
