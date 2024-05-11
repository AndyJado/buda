from helpers import *
import ansa
import buconnect,bumesh

def a_plate_mesh() -> base.Entity:
    curvs = draw_circle(DECK,200)
    face = curve2plane(curvs)
    refs = base.ReferenceEntities(face,True)
    shell_mesh_local(DECK,face)
    one_prop(DECK,None)
    return base.GetEntity(DECK,literals.Entities.PART,2)

if __name__ == "__main__":
    time = NewScript(DECK)

    plate = a_plate_mesh()

    no,nx,ny = (228,205,152)
    cys = buconnect.cre_coord_sys_3node(DECK,no,nx,ny)
    ori = buconnect.dp(no)
    cys2 = buconnect.cre_coord_sys_3node(DECK,9,10,11)
    x,y,z = buconnect.dp(9)

    d_hole = 30.0

    buconnect.local_translate('COPY',cys._id,20,30,20,[plate])
    buconnect.local_translate('COPY',cys._id,20,0,10,[plate])

    bumesh.openhole(DECK,ori,d_hole)
    
    bolt = buconnect.BoltBuilder(DECK)
    bolt.solid_bolt(d_hole,30.0)
    bolt.apply()
    

    # tr = ansa.calc.GetCoordTransformMatrix4x3(DECK,cys,1,1,1)
    # base.TransformMatrix4x3(input_sets_type='NONE',group_offset='',input_function_type='MOVE',pid_offset=0,matrix=tr,entities=[plate])

    time.end()