from helpers import *
import ansa

def a_plate_mesh() -> base.Entity:
    curvs = draw_circle(DECK,200)
    face = curve2plane(curvs)
    refs = base.ReferenceEntities(face,True)
    shell_mesh_local(DECK,face)
    one_prop(DECK,None)
    return base.GetEntity(DECK,literals.Entities.PROPERTY,1)

def node_pos(nid:int):
    nd = base.GetEntity(DECK,literals.Meshes.NODE,nid)
    return list(nd.position)


if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh()

    no,nx,ny = (228,205,152)
    print(node_pos(no))

    # m = ansa.calc.LocalSystem([1,1,0],[0,0,1],[1,1,3])
    # print(m)

    time.end()