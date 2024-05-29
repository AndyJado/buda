import os,sys,datetime,math,re
from typing import Tuple, List
from ansa import base, session, constants, mesh, calc, morph

import buconnect,bumesh,bubase,plugs,buentity,bucreate
from literals import *
from helpers import *

 
if __name__ == "__main__":
    DECK = constants.LSDYNA
    timer = NewScript(DECK)
    ##-----------------------------------
    
    ##--------------------------------
    timer.end()
