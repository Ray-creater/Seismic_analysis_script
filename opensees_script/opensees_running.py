from typing import Iterable
import openseespy.opensees as ops 
import numpy as np

def RectCFSTSteelHysteretic(length:float,secHeight:float,secWidth:float,thickness:float,concrete_grade:float,steel_grade:float,axial_load_ratio:float,disp_control:Iterable[float]):
    '''Peakstress: concrete peak stress \n crushstress: concrete crush stress
    '''
    #disp input
    # dispControl=[3,-3,7,-7,14,-14,14,-14,14,-14,28,-28,28,-28,28,-28,42,-42,42,-42,42,-42,56,-56,0]
    dispControl=tuple(disp_control)
    #Geometry
    # length=740
    # secHeight=100
    # secWidth=100
    # thickness=7
    #Materials
    ##steel_tube
    point1Steel,point2Steel,point3Steel=[460,0.00309],[460,0.02721],[530,0.26969]
    point1SteelNegative,point2SteelNegative,point3SteelNegative=[-460,-0.00309],[-460,-0.02721],[-736,-0.26969]
    pinchX=0.2
    pinchY=0.7
    damagedFactor=0.01
    densitySteel=7.8/1000000000
    ##concrete
    peakPointConcrete,crushPointConcrete=[-221.76,-0.0102],[-195,-0.051]

    unloadingLambda=0.2
    tensileStrength=5.6
    tensilePostStiffness=0.01
    densityConcrete=2.4/1000000000
    #axialLoadRatio
    # axialLoadRatio=0.4
    #fix condition
    Fixed=1
    


    #section parameter
    areaConcrete=(secHeight-2*thickness)*(secWidth-2*thickness)
    areaSteel=secWidth*secHeight-areaConcrete
    

    # fck,Ec,nuConcrete=128.1,4.34*10000,0.21
    # fy,epsilonSteely,Es,nuSteel=444.6,3067/1000000,1.99*100000,0.29
    fck=peakPointConcrete[0]
    fy=point1Steel[0]

    
    #Computate parameter
    axialLoad=(areaConcrete*fck+areaSteel*fy)*axial_load_ratio

    #loading control parameter
    # for item in dispControlPercentage:
    #     dispControl.append(item*length)
    #     dispControl.append(-item*length)
    # print('displist:'dispControl)

    #wipe and build a model
    ops.wipe()
    ops.model('basic','-ndm',2,'-ndf',3)

    #node coordinates
    meshNumLength=5
    meshVerticalSize=length/meshNumLength       
    meshSteelSize=10
    nodes=[(i+1,meshVerticalSize*i) for i in range(int(length/meshVerticalSize)+1)]
    for item in nodes:
        ops.node(item[0],0,item[1])
    
    #boundary condition
    ops.fix(1,1,1,1)
    # if bool(Fixed):
    #     ops.fix(int(length/meshVerticalSize)+1,0,0,1)  ##uppper constrain condition: free or no-rotation 

    #mass defination(concentrate mass to nodes)
    nodeMassSteel=areaSteel*meshVerticalSize*densitySteel
    nodeMassConcrete=areaConcrete*meshVerticalSize*densityConcrete
    nodeMass=nodeMassSteel+nodeMassConcrete
    for i in range(len(nodes)-1):
        arg=[0.,nodeMass,0.]
        ops.mass(i+2,*arg)
    
    #transformation:
    ops.geomTransf('Linear',1)

    #material defination
    ##steel
    
    ops.uniaxialMaterial('Hysteretic',1001,*point1Steel,*point2Steel,*point3Steel,*point1SteelNegative,*point2SteelNegative,*point3SteelNegative,pinchX,pinchY,damagedFactor,0,0.0)
    ##concrete
    ##using concrete01
    #peakPointConcrete,crushPointConcrete=[110.6,0.00544],[22.11,0.09145]
    #ops.uniaxialMaterial('Concrete01',1,*peakPointConcrete,*crushPointConcrete)
    ###using concrete02
    
    ops.uniaxialMaterial('Concrete02',1,*peakPointConcrete,*crushPointConcrete,unloadingLambda,tensileStrength,tensilePostStiffness)

    #section defination
    ops.section('Fiber',1)
    ##inner concrete fiber
    fiberPointI,fiberPointJ=[-(secHeight-2*thickness)/2,-(secWidth-2*thickness)/2],[(secHeight-2*thickness)/2,(secWidth-2*thickness)/2]
    ops.patch('rect',1,10,1,*fiberPointI,*fiberPointJ)    # https://opensees.berkeley.edu/wiki/index.php/Patch_Command 
    ##outside steel fiber
    steelFiberProperty={'height':meshSteelSize,'area':meshSteelSize*thickness}
    steelFiberPropertyLeftAndRight={'height':secWidth,'area':secWidth*thickness}
    ###left and right
    leftEdgeFiberY,rightEdgeFiberY=-(secHeight-2*thickness)/2-thickness/2,(secHeight-2*thickness)/2+thickness/2   #rightEdgeFiberY might be wrong
    leftandRightEdgeFiberZ=[-secWidth/2+steelFiberPropertyLeftAndRight['height']*(1/2+N) for N in range(int(secWidth/steelFiberPropertyLeftAndRight['height']))]
    ###up and down
    upEdgeFiberZ,downEdgeFiberZ=-(secWidth-2*thickness)/2-thickness/2,(secWidth-2*thickness)/2+thickness/2
    upandDownEdgeFiberY=[-secHeight/2+thickness+steelFiberProperty['height']*(1/2+N) for N in range(int((secHeight-2*thickness)/steelFiberProperty['height']))]
    for i in leftandRightEdgeFiberZ:
        i=float(i)
        ops.fiber(float(leftEdgeFiberY),i,steelFiberPropertyLeftAndRight['area'],1001)
        ops.fiber(float(rightEdgeFiberY),i,steelFiberPropertyLeftAndRight['area'],1001)
    for j in upandDownEdgeFiberY:
        j=float(j)
        ops.fiber(j,float(upEdgeFiberZ),steelFiberProperty['area'],1001)
        ops.fiber(j,float(downEdgeFiberZ),steelFiberProperty['area'],1001)
    #beamInergration defination
    ops.beamIntegration('NewtonCotes',1,1,5)

    #element defination
    for i in range(len(nodes)-1):
        ops.element('dispBeamColumn',i+1,i+1,i+2,1,1)

    #recorders
    ops.recorder('Node','-file','topLateralDisp.txt','-time','-node',int(length/meshVerticalSize+1),'-dof',1,2,'disp')
    ops.recorder('Node','-file','topLateralForce.txt','-time','-node',int(length/meshVerticalSize+1),'-dof',1,2,'reaction')
    ops.recorder('Element','-file','topElementForce.txt','-time','-ele',int(length/meshVerticalSize),'force')

    #gravity load
    ops.timeSeries('Linear',1)
    ops.pattern('Plain',1,1)
    ops.load(int(length/meshVerticalSize+1),0,axialLoad,0)
    ops.constraints('Plain')
    ops.numberer('RCM')
    ops.system('BandGeneral')
    ##convertage test
    tolerant,allowedIteralStep=1/1000000,6000
    ops.test('NormDispIncr',tolerant,allowedIteralStep)
    ops.algorithm('Newton')
    ops.integrator('LoadControl',0.1)
    ops.analysis('Static')
    ops.analyze(10)
    ops.loadConst('-time',0)

    #lateraldisp analysis
    ops.pattern('Plain',2,1)
    ops.load(int(length/meshVerticalSize+1),100,0,0)
    for i in range(len(dispControl)):
        if i==0:
            ops.integrator('DisplacementControl',int(length/meshVerticalSize+1),1,0.1)
            ops.analyze(int(dispControl[i]/0.1))
            # print('Working on disp round',i)
        else:
            if dispControl[i]>=0:
                ops.integrator('DisplacementControl',int(length/meshVerticalSize+1),1,0.1)
                ops.analyze(int(abs(dispControl[i]-dispControl[i-1])/0.1))
                # print('Working on disp round',i)
            else:
                ops.integrator('DisplacementControl',int(length/meshVerticalSize+1),1,-0.1)
                ops.analyze(int(abs(dispControl[i]-dispControl[i-1])/0.1))
                # print('Working on disp round',i)


def RectCFSTSteel02(length:float,secHeight:float,secWidth:float,thickness:float,concrete_grade:float,steel_grade:float,axial_load_ratio:float,disp_control:Iterable[float]):
    '''Peakstress: concrete peak stress \n crushstress: concrete crush stress
    '''
    #disp input
    # dispControl=[3,-3,7,-7,14,-14,14,-14,14,-14,28,-28,28,-28,28,-28,42,-42,42,-42,42,-42,56,-56,0]
    dispControl=tuple(disp_control)
    #Geometry
    length=600
    secHeight=100
    secWidth=150
    thickness=18
    #Materials
    ##steel_tube
    fy=444
    Es=148000
    bs=0.001
    R=(10,0.925,0.15)
    densitySteel=7.8/1000000000
    ##concrete
    fc=128.8
    peakPointConcrete,crushPointConcrete=[-221.76,-0.0102],[-195,-0.051]
    unloadingLambda=0.721
    tensileStrength=12.8
    tensilePostStiffness=4340
    densityConcrete=2.4/1000000000
    #axialLoadRatio
    axialLoadRatio=axial_load_ratio
    #fix condition
    Fixed=False
    
    #section parameter
    areaConcrete=(secHeight-2*thickness)*(secWidth-2*thickness)
    areaSteel=secWidth*secHeight-areaConcrete

    # fck,Ec,nuConcrete=128.1,4.34*10000,0.21
    # fy,epsilonSteely,Es,nuSteel=444.6,3067/1000000,1.99*100000,0.29

    #Computate parameter
    axialLoad=(fc*areaConcrete+fy*areaSteel)*axialLoadRatio

    #loading control parameter
    # for item in dispControlPercentage:
    #     dispControl.append(item*length)
    #     dispControl.append(-item*length)
    # print('displist:'dispControl)

    #wipe and build a model
    ops.wipe()
    ops.model('basic','-ndm',2,'-ndf',3)

    #node coordinates
    meshNumLength=10
    meshVerticalSize=length/meshNumLength       
    meshSteelSize=10
    nodes=[(i+1,meshVerticalSize*i) for i in range(int(length/meshVerticalSize)+1)]
    for item in nodes:
        ops.node(item[0],0,item[1])
    
    #boundary condition
    ops.fix(1,1,1,1)
    if bool(Fixed):
        ops.fix(int(length/meshVerticalSize)+1,0,0,1)  ##uppper constrain condition: free or no-rotation 

    #mass defination(concentrate mass to nodes)
    nodeMassSteel=areaSteel*meshVerticalSize*densitySteel
    nodeMassConcrete=areaConcrete*meshVerticalSize*densityConcrete
    nodeMass=nodeMassSteel+nodeMassConcrete
    for i in range(len(nodes)-1):
        arg=[0.,nodeMass,0.]
        ops.mass(i+2,*arg)
    
    #transformation:
    ops.geomTransf('Linear',1) 

    #material defination
    ##steel
    ops.uniaxialMaterial('Steel02',1001,fy,Es,bs,*R,0,1,0,1,0)
    ##concrete
    ##using concrete01
    #peakPointConcrete,crushPointConcrete=[110.6,0.00544],[22.11,0.09145]
    #ops.uniaxialMaterial('Concrete01',1,*peakPointConcrete,*crushPointConcrete)
    ###using concrete02
    
    ops.uniaxialMaterial('Concrete02',1,*peakPointConcrete,*crushPointConcrete,unloadingLambda,tensileStrength,tensilePostStiffness)

    #section defination
    ops.section('Fiber',1)
    ##inner concrete fiber
    fiberPointI,fiberPointJ=[-(secHeight-2*thickness)/2,-(secWidth-2*thickness)/2],[(secHeight-2*thickness)/2,(secWidth-2*thickness)/2]
    ops.patch('rect',1,10,1,*fiberPointI,*fiberPointJ)    # https://opensees.berkeley.edu/wiki/index.php/Patch_Command 
    ##outside steel fiber
    steelFiberProperty={'height':meshSteelSize,'area':meshSteelSize*thickness}
    steelFiberPropertyLeftAndRight={'height':secWidth,'area':secWidth*thickness}
    ###left and right
    leftEdgeFiberY,rightEdgeFiberY=-(secHeight-2*thickness)/2-thickness/2,(secHeight-2*thickness)/2+thickness/2   #rightEdgeFiberY might be wrong
    leftandRightEdgeFiberZ=[-secWidth/2+steelFiberPropertyLeftAndRight['height']*(1/2+N) for N in range(int(secWidth/steelFiberPropertyLeftAndRight['height']))]
    ###up and down
    upEdgeFiberZ,downEdgeFiberZ=-(secWidth-2*thickness)/2-thickness/2,(secWidth-2*thickness)/2+thickness/2
    upandDownEdgeFiberY=[-secHeight/2+thickness+steelFiberProperty['height']*(1/2+N) for N in range(int((secHeight-2*thickness)/steelFiberProperty['height']))]
    for i in leftandRightEdgeFiberZ:
        i=float(i)
        ops.fiber(float(leftEdgeFiberY),i,steelFiberPropertyLeftAndRight['area'],1001)
        ops.fiber(float(rightEdgeFiberY),i,steelFiberPropertyLeftAndRight['area'],1001)
    for j in upandDownEdgeFiberY:
        j=float(j)
        ops.fiber(j,float(upEdgeFiberZ),steelFiberProperty['area'],1001)
        ops.fiber(j,float(downEdgeFiberZ),steelFiberProperty['area'],1001)
    #beamInergration defination
    ops.beamIntegration('NewtonCotes',1,1,5)

    #element defination
    for i in range(len(nodes)-1):
        ops.element('dispBeamColumn',i+1,i+1,i+2,1,1)

    #recorders
    ops.recorder('Node','-file','opensees_script/topLateralDisp.txt','-time','-node',int(length/meshVerticalSize)+1,'-dof',1,2,'disp')
    ops.recorder('Node','-file','opensees_script/topLateralForce.txt','-time','-node',int(length/meshVerticalSize)+1,'-dof',1,2,'reaction')
    ops.recorder('Element','-file','opensees_script/topElementForce.txt','-time','-ele',int(length/meshVerticalSize),'force')
    #gravity load
    ops.timeSeries('Linear',1)
    ops.pattern('Plain',1,1)
    ops.load(int(length/meshVerticalSize+1),0,axialLoad,0)
    ops.constraints('Plain')
    ops.numberer('RCM')
    ops.system('BandGeneral')
    ##convertage test
    tolerant,allowedIteralStep=1/1000000,6000
    ops.test('NormDispIncr',tolerant,allowedIteralStep)
    ops.algorithm('Newton')
    ops.integrator('LoadControl',-0.1)
    ops.analysis('Static')
    ops.analyze(10)
    ops.loadConst('-time',0)

    #lateraldisp analysis
    ops.pattern('Plain',2,1)
    ops.load(int(length/meshVerticalSize+1),100,0,0)
    for i in range(len(dispControl)):
        if i==0:
            ops.integrator('DisplacementControl',int(length/meshVerticalSize)+1,1,0.1)
            ops.analyze(int(dispControl[i]/0.1))
            print('Working on disp round',i)
        else:
            if dispControl[i]-dispControl[i-1]>=0:
                ops.integrator('DisplacementControl',int(length/meshVerticalSize)+1,1,0.1)
                ops.analyze(int(abs(dispControl[i]-dispControl[i-1])/0.1))
                print('Working on disp round',i)
            else:
                ops.integrator('DisplacementControl',int(length/meshVerticalSize+1),1,-0.1)
                ops.analyze(int(abs(dispControl[i]-dispControl[i-1])/0.1))
                print('Working on disp round',i)
    
def extracdata():
    #disp extrac
    with open('opensees_script/topLateralDisp.txt','r') as f:
        text=f.readlines()
    text.pop()
    disp=[]
    for i in text:
        i=i.split(' ')
        disp.append(float(i[1]))
    #force extrac
    with open('opensees_script/topElementForce.txt','r') as f:
        text=f.readlines()
    text.pop()
    force=[]
    for i in text:
        i=i.split(' ')
        force.append(float(i[1])/1000)
    return np.array(disp),np.array(force)

