from helpers import *


if __name__ == "__main__":
    time = NewScript(DECK)
    
    curvs = draw_circle(DECK,200)
    face = curve2plane(curvs)
    refs = base.ReferenceEntities(face,True)
    shell_mesh(DECK,face)
    print(refs)
    # curve = draw_rec(3,3)
    # extrude(curve,3)
    # shell_mesh(DECK,None,1)
    # one_prop(DECK,None)

    time.end()