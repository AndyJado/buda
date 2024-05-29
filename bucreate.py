import os,sys,datetime,math,re
from typing import Tuple, List
from ansa import base, session, constants, mesh, calc, morph

import buconnect,bumesh,helpers,bubase,plugs,buentity
from literals import *

# i'm not proud
DECK = constants.LSDYNA

def cre_rigid_wall(cid:int,vec:tuple) -> base.Entity:
    xt,yt,zt = buconnect.point2global(cid,[0,0,0])
    xh,yh,zh = buconnect.point2global(cid,vec)
    cfg = {'XT':xt,'YT':yt,'ZT':zt,'XH':xh,'YH':yh,'ZH':zh}
    return base.CreateEntity(DECK,'RIGIDWALL_PLANAR',cfg)

def cre_bc1(sid:int)-> base.Entity:
    cfg = {'c':123456,'Use A/LC_POINT DOF':'no','NSID':sid,'BIRTH_DEATH':'OFF'}
    bc = base.CreateEntity(DECK,'BOUNDARY_SPC(SET)',cfg)
    print(bc)
    return bc

def relax_switch(on:bool):
    control = base.CollectEntities(DECK,None,'CONTROL')[0]
    control.set_entity_values(DECK,{'DYNAMIX_RELAXATION_IDRFLG':1})

def relax_switch_off():
    control = base.CollectEntities(DECK,None,'CONTROL')[0]
    control.set_entity_values(DECK,{'DYNAMIX_RELAXATION_IDRFLG':'-999'})

# WARN: time consuming!
# dhole should be a identifier, e.g. 18.033223 and 18.47923 for different bolt  
def cre_hole_from_set(deck:int,sid:int,d_hole:float,search_depth:float):
    hole_set = base.GetEntity(deck,Entities.SET,sid)
    points = base.CollectEntities(deck,hole_set,Meshes.NODE,recursive=True)
    # points = base.CollectEntities(deck,hole_set,Meshes.NODE,) #TRY?
    print('set:',hole_set._name,'hole numbers:',len(points))
    base.DeleteEntity(hole_set,True)
    for point in points:
        bumesh.openhole(deck,point.position,d_hole,search_depth)
    return d_hole
     
def _cre_pretension_curve(d_bolt):
    par = 300 / (d_bolt**2 * math.pi)
    curve = base.CreateLoadCurve("DEFINE_CURVE", {'Name':'pretension', 'SFO': par})
    mat = ((0.0, 0.0),(0.001,300)) #! FIXME!!
    base.SetLoadCurveData(curve, mat)    
    return curve._id
      

def _mod_pretension(deck:int):
    pre = base.CollectEntities(deck, None, "INITIAL_STRESS_SECTION")
    for p in pre:
        p.set_entity_values(deck, {'IZSHEAR':2})

# WARN: time consuming!
def cre_bolt_auto(deck:int,d_bolt:float,len_bolt:float,mat:str,hid=None):
    pre_cid = _cre_pretension_curve(d_bolt)
    bolt = buconnect.BoltBuilder(DECK,hid)
    bolt.solid_bolt(d_bolt,len_bolt,pre_cid)
    bolt.apply()    
    _mod_pretension(deck)
    return bolt

def cre_node(deck,pos:tuple,name=None): 
    return base.CreateEntity(deck,Meshes.NODE,{'Name':name,'X':pos[0],'Y':pos[1],'Z':pos[2]})

# create globle cs: cre_dyna_cs([0,0,0])
def cre_dyna_cs(pos:tuple):
    xo,yo,zo = pos
    return base.CreateEntity(constants.LSDYNA,Entities.COORD,{'DEFINITION METHOD':'ANGLE METHOD','XO':xo,'YO':yo,'ZO':zo})

#TODO: only for metric: N, mm, s
def cre_gravity():
    gravity = base.CreateLoadCurve("DEFINE_CURVE", {'Name':'gravity'})
    grav_data = ((0.0, 1.0), (1000.0, 1.0))
    base.SetLoadCurveData(gravity, grav_data)
    base.CreateEntity(DECK, "LOAD_BODY_OPTION", {'OPTION':'Z', 'apply to':'ALL', 'LCID':gravity._id, 'SF':9810})

def cre_param(deck:int,name:str,val:float) -> base.Entity:
    return base.CreateEntity(deck,Entities.PARAM, {'Name':name, 'Value': val})

def param_set(deck:int,name:str,val):
    para = buentity.get_entity_by_name(deck,name,Entities.PARAM)
    para.set_entity_values(deck,{'Value':val})

#TODO: change and apply later?
def cre_bc(nodes:list[base.Entity]):
    geb = base.CreateGEB(nodes,"GEB_BC")
    geb.set_entity_values(DECK, {'representation':'Spc1','TX':'FIXED','TY':'FREE','TZ':'FREE','RX':'FREE','RY':'FREE','RZ':'FREE'}) 
    base.ApplyGenericEntities(geb)
    return geb


# BUG: won't work!!
#{'Id': 1, 'Type': 'Auto', 'Expression Mode': 'Yes', 'Expression': '1  ', 'Value': '1', 'Local': 'NO', 'Local Name': 'a', 'Name': 'a', 'FROZEN_ID': 'NO', 'FROZEN_DELETE': 'NO', 'DEFINED': 'YES', 'Comment': '', 'Embedded Comment': '', 'MBContainer': None, 'MBContainers': []}
def cre_para_expression(deck:int,name:str,expr:str) -> base.Entity:
    pass
    return base.CreateEntity(deck,Entities.PARAM, {'Name':name, 'Expression Mode': 'Yes','Expression':expr})


def cre_set(deck:int, entities=None, name=None)->base.Entity:
    se = base.CreateEntity(deck, Entities.SET, {'Name': name})
    if entities is not None:
        base.AddToSet(se, entities)
    return se



# create accelerometer asset, FIXME: should call this func early or just make it an asset? BUG: code works but rometer doesn't work good
def accelerometer_addon_cog():
    DECK = constants.LSDYNA
    recrve = helpers.draw_rec(5,5)
    rec = helpers.curve2plane(recrve)
    extru = mesh.VolumesExtrude()
    extru.offset(rec,steps=1,distance=5) #default in Z direction 

    soli = base.CollectEntities(DECK,None,Meshes.SOLID)

    secs = base.CollectEntities(DECK,None,Entities.PROPERTY)

    skin = mesh.CreateShellsOnSolidsPidSkin(soli,True)

    #FIXME: maybe move created to a inclu is a better idea
    base.DeleteEntity(secs+recrve,force=True)

    secs = base.CollectEntities(DECK,None,Entities.PROPERTY)

    assert len(secs) == 1, 'just trying to create a meshed rigid box..'

    sec = secs[0]

    base.CreateEntity(DECK,DynaCards.MAT20,{'MID':1,'DEFINED':'YES'})

    sec.set_entity_values(DECK,{'MID':1})

    base.CreateEntity(DECK,Entities.COORD,{'Name':'S','XO':0,'YO':0,'ZO':0,'XL':1,'YL':0,'ZL':0,'XP':0,'YP':1,'ZP':0})

    base.CreateEntity(DECK,DynaCards.ACCE,{'NID1':1,'NID2':2,'NID3':4,'IGRAV':1})# removed gravity differs how?

    base.CreateEntity(DECK,DynaCards.HISTORY_NODE,{'NODE1':base.GetEntity(DECK,Meshes.NODE,1)})

    base.CreateEntity(DECK,Constrains.EXTRA_NODE,{'TYPE':'PROP','NID':1,'PID':4}) #FIXME: NID change later

    bubase.output('asset/accelerometer.key')

    #TODO: move everything to cid, then move everything to cog except direction

if __name__ == "__main__":
    # timer = helpers.NewScript(DECK)
    ##-----------------------------------
    cds = base.CollectEntities(DECK,None,'BOUNDARY_SPC(SET)')
    print(cds)
    for i in cds:
        print(i.card_fields(DECK,True))
    # ##-----------------------------------
    # timer.end() 
    

