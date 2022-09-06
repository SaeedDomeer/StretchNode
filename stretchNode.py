import sys 
from math import pow,sqrt
from maya import OpenMaya
from maya import OpenMayaMPx

'''
Copy StretchNode.py file to your /maya/plug-ins/ folder.
To load the node use the following command
cmds.loadPlugin("stretchNode.py")
To craete the node use the following command
cmds.createNode('stretchNode')
'''

nodeName = 'stretchNode'
nodeID = OpenMaya.MTypeId(0x00000846)

class stretchNode(OpenMayaMPx.MPxNode):
    
    # Define inputs and output
    enable = OpenMaya.MObject()
    rootPosition = OpenMaya.MObject()
    endPosition = OpenMaya.MObject()
    stretchDistance = OpenMaya.MObject()
    volumePreservation = OpenMaya.MObject()
    output = OpenMaya.MObject()
    
    def __init__(self):
        return OpenMayaMPx.MPxNode.__init__(self)
        
    def compute(self, plug, dataBlock):
        
        # Get inputs data and types
        enableData = dataBlock.inputValue(stretchNode.enable).asFloat()
        rootPositionData = dataBlock.inputValue(stretchNode.rootPosition).asVector()
        endPositionData = dataBlock.inputValue(stretchNode.endPosition).asVector()
        stretchDistanceData = dataBlock.inputValue(stretchNode.stretchDistance).asFloat()
        volumePreservationData = dataBlock.inputValue(stretchNode.volumePreservation).asFloat()
        
        # Calculate the distance betweeen the first joint and last joint
        distanceVal = sqrt(pow(rootPositionData[0]-endPositionData[0],2)+pow(rootPositionData[1]-endPositionData[1],2)+pow(rootPositionData[2]-endPositionData[2],2))
        
        '''
        To create the blend effect, use the following equation: 
        (1 - blender/enableAttribute) * firstInput + blender/enableAttribute * secondInput
        '''
        blendVal = 1 - enableData
        stretchVal = (enableData * distanceVal/stretchDistanceData) + (blendVal * 1)
        
        # Calculate the volume preservation based on the stretch value
        volumePreservationVal = 1/pow(stretchVal,volumePreservationData)
        
        if stretchVal < 1: 
            outputVal = 1
        else:
            outputVal = stretchVal
        
        # Set output data and type
        outputData = dataBlock.outputValue(stretchNode.output)
        outputData.set3Double(outputVal, volumePreservationVal, volumePreservationVal)
        dataBlock.setClean(plug)
            
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(stretchNode())
    
def nodeInitializer():
    
    '''
    Create and attach the node's attributes 
    attributes are readable, writable and storable by default
    '''
    nAttr = OpenMaya.MFnNumericAttribute()
    stretchNode.enable = nAttr.create('enable', 'en', OpenMaya.MFnNumericData.kFloat, 1)
    stretchNode.addAttribute(stretchNode.enable)
    nAttr.setKeyable(True) 
    nAttr.setMin(0)
    nAttr.setMax(1)
    
    stretchNode.rootPosition = nAttr.create('rootPosition', 'rp', OpenMaya.MFnNumericData.k3Double) 
    stretchNode.addAttribute(stretchNode.rootPosition)
    nAttr.setKeyable(True) 
    
    stretchNode.endPosition = nAttr.create('endPosition', 'ep', OpenMaya.MFnNumericData.k3Double)  
    stretchNode.addAttribute(stretchNode.endPosition)
    nAttr.setKeyable(True) 
    
    stretchNode.volumePreservation = nAttr.create('volumePreservation', 'vol', OpenMaya.MFnNumericData.kFloat, 1)
    stretchNode.addAttribute(stretchNode.volumePreservation)   
    nAttr.setKeyable(True)
     
    stretchNode.stretchDistance = nAttr.create('stretchDistance', 'strDis', OpenMaya.MFnNumericData.kFloat, 1)
    stretchNode.addAttribute(stretchNode.stretchDistance)
    nAttr.setKeyable(True) 
    nAttr.setMin(0.001)
    
    stretchNode.output = nAttr.create("output", "out", OpenMaya.MFnNumericData.k3Double)
    stretchNode.addAttribute(stretchNode.output)
    nAttr.setWritable(False)   
    nAttr.setStorable(False)   
    nAttr.setKeyable(False) 

    # Create node's connections
    stretchNode.attributeAffects(stretchNode.enable, stretchNode.output)
    stretchNode.attributeAffects(stretchNode.rootPosition, stretchNode.output)
    stretchNode.attributeAffects(stretchNode.endPosition, stretchNode.output)
    stretchNode.attributeAffects(stretchNode.volumePreservation, stretchNode.output)
    stretchNode.attributeAffects(stretchNode.stretchDistance, stretchNode.output)

def initializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject, 'SaeedDomeer', '1.0')
    try:
        mPlugin.registerNode(nodeName, nodeID, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register: " + nodeName)
        
def uninitializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject)
    try:
        mPlugin.deregisterNode(nodeID)
    except:
        sys.stderr.write("Failed to deregister:" + nodeName)
        
