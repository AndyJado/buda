from enum import Enum

class Entities(str, Enum):
    ALL: str ='__ALL_ENTITIES__'
    PART: str = 'ANSAPART'
    PROPERTY: str = '__PROPERTIES__'
    MATERIAL: str = '__MATERIALS__'
    SET: str = 'SET'
    CONTACT: str = 'CONTACT'
    SEGMENT: str = 'SEGMENT'
    PARAM: str = 'A_PARAMETER'
    CURVE: str = 'CURVE'
    FACE: str = 'FACE'
    # FIXME: there are other CS type beyond SYSTEM, can change though
    COORD: str = 'DEFINE_COORDINATE_SYSTEM'
    INCLUDE: str = 'INCLUDE'
    CONNECT: str = '__CONNECTIONS__'

class Constrains(str,Enum):
    EMASS: str = 'ELEMENT_MASS'
    REVOLUTE: str = 'CONSTRAINED_JOINT_REVOLUTE'
    NODE: str = 'CONSTRAINED_NODAL_RIGID_BODY'
    EXTRA_NODE: str = 'CONSTRAINED_EXTRA_NODES_NODE'
    EXTRA_NSET: str = 'CONSTRAINED_EXTRA_NODES_SET'
    DISCRETE: str = 'CONSTRAINED_JOINT_CYLINDRICAL'
    CYLINDER: str = 'CONSTRAINED_JOINT_CYLINDRICAL'

class Meshes(str, Enum):
    NODE: str = 'NODE'
    ELEMENT: str = '__ELEMENTS__'
    SOLID: str = 'ELEMENT_SOLID'
    SHELL: str = 'ELEMENT_SHELL'

class DynaCards(str, Enum):
    SOLID: str= 'SECTION_SOLID'
    SHELL: str= 'SECTION_SHELL'
    MAT1: str = 'MAT1 MAT_ELASTIC'
    MAT20: str ='MAT20 MAT_RIGID'
    ACCE: str = 'ELEMENT_SEATBELT_ACCELEROMETER'
    HISTORY_NODE: str = 'DATABASE_HISTORY_NODE'
    VELOCITY_GEN: str = 'INITIAL_VELOCITY_GENERATION'

# FIXME: damn, what about nega?
class Ax(int,Enum):
    X = 0
    Y = 1
    Z = 2

    @staticmethod
    def get_vec(axis):
        if axis == Ax.X:
            return [1, 0, 0]
        elif axis == Ax.Y:
            return [0, 1, 0]
        elif axis == Ax.Z:
            return [0, 0, 1]

    def vec(self):
        return self.get_vec(self)

class Boundary(str, Enum):
    SPC_SET: str = 'BOUNDARY_SPC(SET)'
    MOTION: str = 'BOUNDARY_PRESCRIBED_MOTION'