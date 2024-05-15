from enum import Enum

class Entities(str, Enum):
    # ALL: str ='__ALL_ENTITIES__'
    PART: str = 'ANSAPART'
    PROPERTY: str = '__PROPERTIES__'
    MATERIAL: str = '__MATERIALS__'
    SET: str = 'SET'
    CONTACT: str = 'CONTACT'
    SEGMENT: str = 'SEGMENT'
    PARAM: str = 'A_PARAMETER'
    CURVE: str='CURVE'
    # FIXME: there are other CS type beyond SYSTEM, can change though
    COORD: str = 'DEFINE_COORDINATE_SYSTEM'
    INCLUDE: str = 'INCLUDE'

class Meshes(str, Enum):
    NODE: str = 'NODE'
    ELEMENT: str = '__ELEMENTS__'
    SOLID: str = 'ELEMENT_SOLID'
    SHELL: str = 'ELEMENT_SHELL'

class DynaCards(str, Enum):
    SHELL: str= 'SECTION_SHELL'
    MAT1: str = 'MAT1 MAT_ELASTIC'
