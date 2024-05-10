from helpers import *


if __name__ == "__main__":
    time = NewScript(DECK)
    
    curve = cre_quad(3,3)
    extrude(curve,3)
    shell_mesh(DECK,None,1)
    one_prop(DECK,None)

    time.end()