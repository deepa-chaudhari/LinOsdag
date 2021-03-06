'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
import cmath
import math
from PyQt4.QtCore import QString
import numpy as np
from numpy import math
from model import *



class cleatCommonData(object):
    
    def __init__(self, inputObj,outputObj,dictBeamdata,dictColumndata,dictAngleData):
        '''
        Provide all the data related to Finplate connection
        
        :param inputObj:
        :type inputObj:dictionary(Input parameter dictionary)
        :param outputObj:
        :type ouputObj :dictionary (output parameter dictionary)
        :param dictBeamdata :
        :type dictBeamdata:  dictionary (Beam sectional properties) 
        :param dictColumndata :
        :type dictBeamdata: dictionary (Column sectional properties dictionary)

        '''
        self.beam_T = float(dictBeamdata[QString("T")])
        self.col_T = float(dictColumndata[QString("T")])
        self.D_beam = int (dictBeamdata[QString("D")])
        self.D_col = int (dictColumndata[QString("D")])
        self.col_B = int(dictColumndata[QString("B")])
        self.beam_B = int(dictBeamdata[QString("B")])
        self.col_tw = float(dictColumndata[QString("tw")])
        self.beam_tw = float(dictBeamdata[QString("tw")])
        self.col_Designation = dictColumndata[QString("Designation")]
        self.beam_Designation = dictBeamdata[QString("Designation")]
        self.beam_R1 = float(dictBeamdata[QString("R1")])
        self.col_R1 = float(dictColumndata[QString("R1")])
        self.cleat_ht = outputObj['cleat']["height"]
        self.cleat_legsize= int(dictAngleData[QString("A")])
        self.cleat_legsize_1 = int(dictAngleData[QString("B")])
#         self.cleat_legsize_1 = 120
        self.cleat_thk = int(dictAngleData[QString("t")])
#         self.plate_ht= outputObj['Plate']['height'] 
#         self.cleat_thk = inputObj['Plate']["Thickness (mm)"]

#         self.plate_width = outputObj['Plate']['width']
#         self.cleat_thk = outputObj['Plate']['height']
#         self.cleat_thk =  outputObj['Weld']['thickness']
        self.bolt_dia  = inputObj["Bolt"]["Diameter (mm)"]
        self.bolt_type  = inputObj["Bolt"]["Type"]
        self.bolt_grade = inputObj['Bolt']['Grade']        
        self.connectivity =  inputObj['Member']['Connectivity']
        self.pitch = outputObj['Bolt']["pitch"]
        self.gauge = outputObj['Bolt']["gauge"]
        self.end_dist = outputObj['Bolt']["enddist"]
        self.edge_dist = outputObj['Bolt']["edge"]
        self.no_of_rows = outputObj['Bolt']["numofrow"] 
        self.no_of_col = outputObj['Bolt']["numofcol"]
        self.no_of_crows =  outputObj['cleat']['numofrow']
        self.no_of_ccol = outputObj['cleat']['numofcol']
        self.cpitch = outputObj['cleat']['pitch']
        self.cgauge = outputObj['cleat']['guage']
        self.cedge_dist = outputObj['cleat']['edge']
        self.cend_dist = outputObj['cleat']['end']
        self.col_L = 800
        self.beam_L = 350
        self.gap = 20 # Clear distance between Column and Beam as per subramanyam's book ,range 15-20 mm
        self.notch_L = (self.col_B/2 - self.col_tw/2) + 10
        self.notch_offset = (self.col_T + self.col_R1)
    
        
    def addSMarker(self, dwg):
        '''
        Draws start arrow to given line  -------->
        
        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)
        
        '''
        
        smarker = dwg.marker(insert=(8,3), size=(30,30),orient="auto")
        
        smarker.add(dwg.path(d =" M0,0 L3,3 L0,6 L8,3 L0,0", fill='black'))
        dwg.defs.add(smarker)
        
        #smarker = dwg.marker(insert=(-8,0), size =(30,20), orient="auto")
        #smarker.add(dwg.polyline([(-2.5,0), (0,3), (-8,0), (0,-3)], fill='black'))
        #smarker.add(dwg.polyline([(0,0), (3,3), (0,6), (8,3),(0,0)], fill='black'))
        
        return smarker
    
    def addSectionMarker(self, dwg):
        '''
        Draws start arrow to given line  -------->
        
        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)
        
        '''
        sectionMarker = dwg.marker(insert=(0,5), size=(10,10),orient="auto")
        sectionMarker.add(dwg.path(d = "M 0 0 L 10 5 L 0 10 z", fill='blue',stroke= 'black'))
        dwg.defs.add(sectionMarker)
        
        return sectionMarker
    
    
    def addEMarker(self, dwg):
        '''
        This routine returns end arrow  <---------
        
        :param dwg :
        :type dwg : svgwrite  ( Container for all svg elements)
        
        '''
        #emarker = dwg.marker(insert=(8,0), size =(30,20), orient="auto")
        emarker = dwg.marker(insert=(0,3), size=(30,20),orient="auto")
        #emarker.add(dwg.polyline([(2.5,0), (0,3), (8,0), (0,-3)], fill='black'))
        #emarker.add(dwg.polyline([(0,3), (8,6), (5,3), (8,0),(0,3)], fill='black'))
        #emarker.add(dwg.path(d="M2,2 L2,13 L8,7 L2,2"", fill='red'))
        emarker.add(dwg.path(d =" M0,3 L8,6 L5,3 L8,0 L0,3", fill='black'))
        dwg.defs.add(emarker)
        return emarker
    
    def drawArrow(self,line,s_arrow,e_arrow):
        line['marker-start'] = s_arrow.get_funciri()
        line['marker-end'] = e_arrow.get_funciri()

    def drawStartArrow(self,line,s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def drawEndArrow(self,line,e_arrow):
        line['marker-end'] = e_arrow.get_funciri()
    
    def drawFaintLine(self,ptOne,ptTwo,dwg):
        '''
        Draw faint line to show dimensions.
        
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptOne :
        :type NumPy Array
        :param ptTwo :
        :type NumPy Array
        
        '''
        dwg.add(dwg.line(ptOne,ptTwo).stroke('#D8D8D8',width = 2.5,linecap = 'square',opacity = 0.7))
        
    
    def draw_dimension_outerArrow(self, dwg, pt1, pt2, text, params):  
          
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: pt1 :
        :type NumPy Array
        :param pt2 :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["offset"] :
        :type params["offset"] : offset of the dimension line
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["lineori"]: 
        :type params ["lineori"]: String (right/left) 
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)       
        '''
        smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)  

        lineVec = pt2 - pt1 # [a, b]
        normalVec = np.array([-lineVec[1], lineVec[0]]) # [-b, a]
        normalUnitVec = self.normalize(normalVec)
        if(params["lineori"] == "left"):
            normalUnitVec = -normalUnitVec
            
        # Q1 = pt1 + params["offset"] * normalUnitVec
        # Q2 = pt2 + params["offset"] * normalUnitVec
        Q1 = pt1 + params["offset"] * normalUnitVec
        Q2 = pt2 + params["offset"] * normalUnitVec
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width = 2.5, linecap = 'square'))
        self.drawStartArrow(line, emarker)
        self.drawEndArrow(line, smarker)

        Q12mid = 0.5 * (Q1 + Q2)
        txtPt = Q12mid + params["textoffset"] * normalUnitVec
        dwg.add(dwg.text(text, insert=(txtPt), fill='black',font_family = "sans-serif",font_size = 28))
        
        L1 = Q1 + params["endlinedim"] * normalUnitVec
        L2 = Q1 + params["endlinedim"]* (-normalUnitVec)
        dwg.add(dwg.line(L1,L2).stroke('black',width = 2.5,linecap = 'square',opacity = 1.0))
        L3 = Q2 + params["endlinedim"] * normalUnitVec
        L4 = Q2 + params["endlinedim"]* (-normalUnitVec)
        dwg.add(dwg.line(L3,L4).stroke('black',width = 2.5,linecap = 'square',opacity = 1.0))
        
    def normalize(self, vec):
        a = vec[0]
        b = vec[1]
        mag = math.sqrt(a * a + b * b)
        return vec / mag
    
    def draw_cross_section(self,dwg,ptA,ptB,txtPt,text):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param ptA :
        :type ptA : NumPy Array
        :param ptB :
        :type ptB : NumPy Array
        :param txtPt :
        :type txtPt : NumPy Array
        :param text :
        :type text : String
        
        '''
        line = dwg.add(dwg.line((ptA),(ptB)).stroke('black',width = 2.5,linecap = 'square'))
        sec_arrow = self.addSectionMarker(dwg)
        self.drawEndArrow(line,sec_arrow)
        dwg.add(dwg.text(text, insert=(txtPt), fill='black',font_family = "sans-serif",font_size = 52))
    
        
    def draw_dimension_innerArrow(self, dwg, ptA, ptB, text, params):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param ptB :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)   
        :param params["arrowlen"]:
        :type params["arrowlen"]: float (Size of the arrow)
        '''
        
        #smarker = self.addSMarker(dwg)
        #emarker = self.addEMarker(dwg)  
        smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)  
        
        u = ptB - ptA # [a, b]
        uUnit = self.normalize(u)
        
        vUnit = np.array([-uUnit[1], uUnit[0]]) # [-b, a]
        
        A1 = ptA + params["endlinedim"] * vUnit
        A2 = ptA - params["endlinedim"]* (-vUnit)
        dwg.add(dwg.line(A1,A2).stroke('black',width = 2.5,linecap = 'square'))
        B1 = ptB + params["endlinedim"] * vUnit
        B2 = ptB - params["endlinedim"]* (-vUnit)
        dwg.add(dwg.line(B1,B2).stroke('black',width = 2.5,linecap = 'square'))
        A3 = ptA - params["arrowlen"]* uUnit
        B3 = ptB + params["arrowlen"]* uUnit
        
        line = dwg.add(dwg.line(A3, ptA).stroke('black', width = 2.5, linecap = 'square'))
        self.drawEndArrow(line, smarker)
        #self.drawStartArrow(line, emarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width = 2.5, linecap = 'butt'))
        self.drawEndArrow(line, smarker)
        #self.drawStartArrow(line, emarker)
        txtPt = B3 + params["textoffset"] * uUnit
        dwg.add(dwg.text(text, insert=(txtPt), fill='black',font_family = "sans-serif",font_size = 28))
        
    
        
        
    def drawOrientedArrow(self, dwg, pt, theta, orientation, offset, textUp,textDown):
    
        '''
        Drawing an arrow on given direction 
        
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param theta: 
        :type theta : Int
        :param orientation :
        :type orientation : String
        :param offset :
        :type offset : float
        :param textUp :
        :type textUp : String
        :param textDown :
        :type textup : String
        
        '''
        #Right Up.
        theta = math.radians(theta)
        charWidth = 16
        xVec = np.array([1, 0])
        yVec = np.array([0, 1])
        
        p1 = pt
        lengthA = offset / math.sin(theta)
        
        arrowVec = None
        if(orientation == "NE"):
            arrowVec = np.array([-math.cos(theta), math.sin(theta)])
        elif(orientation == "NW"):
            arrowVec = np.array([math.cos(theta), math.sin(theta)])
        elif(orientation == "SE"):
            arrowVec = np.array([-math.cos(theta), -math.sin(theta)])
        elif(orientation == "SW"):
            arrowVec = np.array([math.cos(theta), -math.sin(theta)])
            
        p2 = p1 - lengthA * arrowVec
        
        text = textDown if len(textDown) > len(textUp) else textUp
        lengthB = len(text) * charWidth
        
        labelVec = None
        if(orientation == "NE"):
            labelVec = -xVec
        elif(orientation == "NW"):
            labelVec = xVec
        elif(orientation == "SE"):
            labelVec = -xVec
        elif(orientation == "SW"):
            labelVec = xVec

        
        p3 = p2 + lengthB * (-labelVec)
            
        txtOffset = 18
        offsetVec = - yVec

        txtPtUp = None
        if(orientation == "NE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) -  (txtOffset + 15) * offsetVec
        elif(orientation == "NW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec
        elif(orientation == "SE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - txtOffset * offsetVec
        elif(orientation == "SW"):
            txtPtUp = p3 + 0.1 * lengthB  * labelVec + (txtOffset ) * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec
        
        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill= 'none', stroke='black', stroke_width = 2.5))
        
        
        #smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)
        #self.drawStartArrow(line, smarker)
        self.drawStartArrow(line, emarker)
        
        dwg.add(dwg.text(textUp, insert=(txtPtUp), fill='black',font_family = "sans-serif",font_size = 28))
        dwg.add(dwg.text(textDown, insert=(txtPtDwn), fill='black',font_family = "sans-serif",font_size = 28))
    
    def saveToSvg(self,fileName,view):
        '''
         It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web
        
        '''
        fin2DFront = cleat2DCreatorFront(self)
        fin2DTop = cleat2DCreatorTop(self)
        fin2DSide = cleat2DCreatorSide(self)
        
        if self.connectivity == 'Column flange-Beam web':
            if view == "Front":
                fin2DFront.callCFBWfront(fileName)
            elif view == "Side":
                fin2DSide.callCFBWSide(fileName)
            elif view == "Top":
                fin2DTop.callCFBWTop(fileName)
            else:
                fileName = 'output/cleatangle/Report/cleatFront.svg'
                fin2DFront.callCFBWfront(fileName)
                fileName = 'output/cleatangle/Report/cleatSide.svg'
                fin2DSide.callCFBWSide(fileName)
                fileName = 'output/cleatangle/Report/cleatTop.svg'
                fin2DTop.callCFBWTop(fileName)
                
            
        elif self.connectivity == 'Column web-Beam web':
            if view == "Front":
                fin2DFront.callCWBWfront(fileName)
            elif view =="Side":
                fin2DSide.callCWBWSide(fileName)
            elif view == "Top":
                fin2DTop.callCWBWTop(fileName)
            else:
                fileName = 'output/cleatangle/Report/cleatFront.svg'
                fin2DFront.callCWBWfront(fileName)
                fileName = 'output/cleatangle/Report/cleatSide.svg'
                fin2DSide.callCWBWSide(fileName)
                fileName = 'output/cleatangle/Report/cleatTop.svg'
                fin2DTop.callCWBWTop(fileName)
            
        else:
            if view == "Front":
                fin2DFront.callBWBWfront(fileName)
            elif view =="Side":
                fin2DSide.callBWBWSide(fileName)
            elif view == "Top":
                fin2DTop.callBWBWTop(fileName)
            else:
                fileName = 'output/cleatangle/Report/cleatFront.svg'
                fin2DFront.callBWBWfront(fileName)
                fileName = 'output/cleatangle/Report/cleatSide.svg'
                fin2DSide.callBWBWSide(fileName)
                fileName = 'output/cleatangle/Report/cleatTop.svg'
                fin2DTop.callBWBWTop(fileName)

class cleat2DCreatorFront(object):
    
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        
        self.A2 =(self.dataObj.col_B,(self.dataObj.col_L-self.dataObj.D_beam)/2)
        self.B = (self.dataObj.col_B,0)
        self.A = (0,0)
        self.D = (0,self.dataObj.col_L)
        self.C = (self.dataObj.col_B,self.dataObj.col_L)
        self.B2 = (self.dataObj.col_B,(self.dataObj.D_beam + self.dataObj.col_L)/2)
        
        ptEx = (self.dataObj.col_B-self.dataObj.col_tw)/2
        ptEy = 0.0
        self.E = (ptEx,ptEy)
        
        ptHx = (self.dataObj.col_B-self.dataObj.col_tw)/2
        ptHy = self.dataObj.col_L
        self.H = (ptHx,ptHy)
        
        ptFx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptFy = 0
        self.F = (ptFx,ptFy)
        
        ptGx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptGy = self.dataObj.col_L
        self.G = np.array([ptGx,ptGy])
        
        #Draw rectangle for finPlate PRSU
        ptPx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptPy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.P = (ptPx,ptPy) 
        self.ptP = np.array([ptPx,ptPy])
        
        self.U = self.ptP + (self.dataObj.cleat_ht) * np.array([0,1])
        
        ptRx = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.cleat_legsize
        ptRy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.R = (ptRx,ptRy)
        
        ptSx = ptRx
        ptSy = ptPy + self.dataObj.cleat_ht
        self.S = (ptSx,ptSy)
        
        ptC1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptC1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.C1 =np.array([ptC1x,ptC1y])
        
        ptA1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptA1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2)
        self.A1 = np.array([ptA1x,ptA1y])
        
        ptA3x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap) + self.dataObj.beam_L
        ptA3y = ((self.dataObj.col_L - self.dataObj.D_beam)/2)
        self.A3 = (ptA3x,ptA3y)
        
        ptB3x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap) + self.dataObj.beam_L
        ptB3y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 ) 
        self.B3 = (ptB3x,ptB3y)
        
        ptB1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptB1y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 ) 
        self.B1 = np.array([ptB1x,ptB1y])
        self.ptB1 = np.array([ptB1x,ptB1y])
        
        ptC2x= ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20)
        ptC2y = ptC1y + self.dataObj.cleat_ht
        self.C2 = (ptC2x,ptC2y)
        
        ptA5x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20)
        ptA5y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + self.dataObj.beam_T
        self.A5 = ptA5x,ptA5y
        
        ptA4x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20) + self.dataObj.beam_L
        ptA4y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + self.dataObj.beam_T
        self.A4 = (ptA4x,ptA4y)
        
        ptB4x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20) + self.dataObj.beam_L
        ptB4y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 )  - self.dataObj.beam_T  
        self.B4 = (ptB4x,ptB4y)
        
        ptBx5 = ((self.dataObj.col_B +        
        self.dataObj.col_tw)/2) + 20
        ptBy5 = ((self.dataObj.col_L + self.dataObj.D_beam)/2 )  - self.dataObj.beam_T
        self.B5 = (ptBx5,ptBy5)
        
        ptP1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist)
        ptP1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 +(self.dataObj.col_tw + self.dataObj.beam_R1 + 3)+ self.dataObj.end_dist)
        self.P1 = (ptP1x,ptP1y)
        

        #### Column flange points for column flange beam web connectivity #####
        
        fromPlate_pt = self.dataObj.D_col + self.dataObj.gap # 20 mm clear distance between colume and beam
        ptFAx = 0
        ptFAy = 0
        self.FA = (ptFAx,ptFAy)
         
        ptFEx = self.dataObj.col_T
        ptFEy = 0.0
        self.FE =(ptFEx,ptFEy)
         
        ptFFx = self.dataObj.D_col - self.dataObj.col_T
        ptFFy = 0.0
        self.FF =(ptFFx,ptFFy)
         
        ptFBx = self.dataObj.D_col 
        ptFBy = 0.0
        self.FB =(ptFBx,ptFBy)
         
        ptFCx = self.dataObj.D_col
        ptFCy = self.dataObj.col_L
        self.FC = np.array([ptFBx,ptFCy])
         
        ptFGx = self.dataObj.D_col - self.dataObj.col_T
        ptFGy = self.dataObj.col_L
        self.FG =(ptFGx,ptFGy)
         
        ptFHx = self.dataObj.col_T
        ptFHy = self.dataObj.col_L
        self.FH =(ptFHx,ptFHy)
         
        ptFDx = 0.0
        ptFDy = self.dataObj.col_L
        self.FD =(ptFDx,ptFDy)
        
        ptFPx = self.dataObj.D_col
        ptFPy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FP = (ptFPx,ptFPy)
        self.ptFP = np.array([ptFPx,ptFPy])
        
        self.FW = self.FP + self.dataObj.cleat_thk * np.array([1,0])
        
        ptFUx = self.dataObj.D_col
        ptFUy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        self.FU = (ptFUx,ptFUy)
        
        
        #FC1
        ptFC1x = fromPlate_pt 
        ptFC1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])
        
        #FC2
        ptFC2x = fromPlate_pt
        ptFC2y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) +( self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        self.FC2 = (ptFC2x, ptFC2y)
        
        #FA1
        ptFA1x = fromPlate_pt
        ptFA1y = (self.dataObj.col_L - self.dataObj.D_beam)/2
        self.FA1 = np.array([ptFA1x, ptFA1y])
        
        #FA4
        ptFA4x = fromPlate_pt
        ptFA4y = (self.dataObj.col_L - self.dataObj.D_beam)/2  + self.dataObj.beam_T
        self.FA4 = ptFA4x, ptFA4y
        
        #FA2
        ptFA2x = ptFC1x + self.dataObj.beam_L
        ptFA2y = ptFA1y
        self.FA2 = np.array([ptFA2x, ptFA2y])
        
        #FA3
        ptFA3x = fromPlate_pt  + self.dataObj.beam_L
        ptFA3y = (((self.dataObj.col_L - self.dataObj.D_beam)/2 ) + self.dataObj.beam_T) 
        self.FA3 = ptFA3x, ptFA3y
        
        #FB3
        ptFB3x = fromPlate_pt + self.dataObj.beam_L
        ptFB3y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB3 = (ptFB3x, ptFB3y)
        
        
        #FB2
        ptFB2x = fromPlate_pt + self.dataObj.beam_L
        ptFB2y = (self.dataObj.col_L -self.dataObj.D_beam)/2 +  self.dataObj.D_beam 
        self.FB2 = ptFB2x, ptFB2y
        
        #FB1
        ptFB1x = self.dataObj.D_col + self.dataObj.gap
        ptFB1y = (self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam 
        self.FB1 = np.array([ptFB1x, ptFB1y])
                

        
        #FB4
        ptFB4x = fromPlate_pt
        ptFB4y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB4 = ptFB4x, ptFB4y
        
        ##### Points for Beam-Beam connection ######
        
        # for primary beam
        self.BA = (0,0)
        self.BB = self.BA + (self.dataObj.col_B) * np.array([1,0])
        self.BC = self.BB + (self.dataObj.col_T) * np.array([0,1])
        self.BD = self.BC - (self.dataObj.col_B - self.dataObj.col_tw)/2 * np.array([1,0])
        self.BE = self.BD + (self.dataObj.D_col - 2*self.dataObj.col_T) * np.array([0,1])
        self.BF = self.BC + (self.dataObj.D_col - 2*self.dataObj.col_T) * np.array([0,1])
        self.BG = self.BF + (self.dataObj.col_T) * np.array([0,1])
        self.BH = self.BG - (self.dataObj.col_B) * np.array([1,0])
        self.BI = self.BH - (self.dataObj.col_T) * np.array([0,1])
        self.BJ = self.BI + (self.dataObj.col_B - self.dataObj.col_tw)/2 * np.array([1,0])
        self.BK = self.BJ - (self.dataObj.D_col - 2*self.dataObj.col_T) * np.array([0,1])
        self.BL = self.BI - (self.dataObj.D_col - 2*self.dataObj.col_T) * np.array([0,1])
        
        # for secondary beam
        self.D_notch = self.dataObj.col_T + self.dataObj.col_R1
        self.BA1 = self.BB + 10 * np.array([1,0])
        self.BA2 = self.BA1 + (self.dataObj.beam_L - 10 - self.dataObj.col_B/2  + self.dataObj.col_tw/2 +  self.dataObj.gap) * np.array([1,0])
        self.BB2 = self.BA2 + self.dataObj.D_beam * np.array([0,1])
        self.BB1 = self.BB2 - self.dataObj.beam_L * np.array([1,0])
        self.BA4 = self.BA1 + self.dataObj.beam_T * np.array([0,1])
        self.BA3 = self.BA2 + self.dataObj.beam_T * np.array([0,1])
        self.BB3 = self.BB2 - self.dataObj.beam_T * np.array([0,1])
        self.BB4 = self.BB1 - self.dataObj.beam_T * np.array([0,1])
        self.BC1 = self.BB1 - (self.dataObj.D_beam - self.dataObj.notch_offset) * np.array([0,1])
        self.BC2 = self.BC1 + self.dataObj.cleat_ht * np.array([0,1])
        self.BA5 = self.BA1 + self.dataObj.notch_offset * np.array([0,1])
        
        #for cleat angle
        
        self.BP = self.BC1 - self.dataObj.gap * np.array([1,0])
        self.BQ = self.BP + self.dataObj.cleat_thk * np.array([1,0])
        self.BR = self.BP + self.dataObj.cleat_legsize * np.array([1,0]) 
        self.BP1 = self.BP + self.dataObj.cleat_ht * np.array([0,1]) 
        self.BQ1 = self.BP1 + self.dataObj.cleat_thk * np.array([1,0])
        self.BR1 = self.BP1 + self.dataObj.cleat_legsize * np.array([1,0])      
        
    def callBWBWfront(self,fileName):
        v_height = self.dataObj.D_col + 850
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0,1])
#         dwg = svgwrite.Drawing(fileName, size=('1200mm', '1225mm'), viewBox=('-500 -250 1500 1225'))
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-500 -350 1500 ' +str(v_height)))
        
        ################# Cross section A-A ##################
        ptSecA = self.BA + (320 * np.array([0,-1]))
        ptSecB = ptSecA + (50 * np.array([0,1]))
        txtpt = ptSecB +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = self.BA2 + (320 * np.array([0,-1]))
        ptSecD = ptSecC + (50 * np.array([0,1]))
        txtpt = ptSecD +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        #############################################################################
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        dwg.add(dwg.polyline(points = [(self.BA),(self.BB),(self.BC),(self.BD),(self.BE),(self.BF),(self.BG),(self.BH),(self.BI),(self.BJ),(self.BK),(self.BL),(self.BA)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
#         dwg.add(dwg.polyline(points = [(self.BC1),(self.BA5),(self.BA1),(self.BA2),(self.BB2),(self.BB1),(self.BB4),(self.BC2)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.polyline(points = [(pt1),(self.BA1),(self.BA2),(self.BB2),(self.BB1),(self.BB4),(self.BC2)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.BC1),(self.BC2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.BA4),(self.BA3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.BB4),(self.BB3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BQ), size=((self.dataObj.cleat_legsize-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
#         "M10 10 C 20 20, 40 20, 50 10"
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0,1])
        pt2 = self.BA5 - self.dataObj.col_R1 * np.array([1,0])
        
#         d=[]
#         d.append("M")
#         d.append(pt1)
#         d.append("C")
#         d.append(self.BA5)
#         d.append(",")
#         d.append(self.BA5)
#         d.append(",")
#         d.append(pt2)
        d=[]
        d.append("M")
        d.append(pt1)
        d.append("A")
        d.append(np.array([self.dataObj.col_R1,self.dataObj.col_R1]))
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("1")
        d.append(",")
        d.append(pt2)
        dwg.add(dwg.path(d =d,  stroke="blue",fill = "none",stroke_width="2.5")) 
#         d="M80 230
#            A 45 45, 0, 0, 1, 125 275
#            L 125 230 Z" fill="purple"
       
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []

        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.BP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0]) + self.dataObj.edge_dist * np.array ([0,1]) + \
                    (i-1) * self.dataObj.pitch * np.array([0,1]) + (j-1) * self.dataObj.gauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                
                ptE = pt - (bolt_r + 4) * np.array([0,1])
                PtF = pt + (bolt_r + 4) * np.array([0,1])
                dwg.add(dwg.line((ptE),(PtF)).stroke('red',width = 2.0,linecap = 'square'))
#                 ptE = self.ptFP + self.dataObj.edge_dist * np.array([1,0]) +(j-1) * self.dataObj.gauge * np.array([1,0])
#                 ptF = ptE + self.dataObj.cleat_ht * np.array([0,1])
#                 dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))   
                colList.append(pt)
            ptList.append(colList)
        
        
        for i in range(1,(nr_c+1)):
            pt_c = self.BP + self.dataObj.cedge_dist * np.array([0,1]) - self.dataObj.col_tw * np.array([1,0]) + (i-1) * self.dataObj.cpitch * np.array([0,1])
            pt1_c = pt_c - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill= "black", stroke='black', stroke_width=2.0))
            pt_B1 = pt_c - 10 * np.array([1,0])
            pt_B2 = pt_c + (self.dataObj.col_T + self.dataObj.cleat_thk + 10) * np.array([1,0])
            dwg.add(dwg.line((pt_B1),(pt_B2)).stroke('black',width = 2.0,linecap = 'square'))
            ptList_c.append(pt_c)    
        
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])

        
        #Included cleat height and pitch details of column bolt group
        # Drawing faint lines at right top and bottom corners of cleat
#         rt1 = self.FP + self.dataObj.cleat_legsize * np.array([1,0])
        rt2 = self.BR + (self.dataObj.beam_L + 150 - self.dataObj.gauge) * np.array([1,0])
        self.dataObj.drawFaintLine(self.BR, rt2, dwg)
#         rb1 = rt1 + self.dataObj.cleat_ht * np.array([0,1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0,1])
        self.dataObj.drawFaintLine(self.BR1, rb2, dwg)
        #drawing inner arrow to represent cleat height
        params = {"offset": self.dataObj.beam_L , "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.BR, self.BR1,  str(int(self.dataObj.cleat_ht)), params)
        
        ############################BEAM CONNECTIVITY MARKING###############################
        # Drawing faint lines at bolt groups on Beam
        bt1 = np.array(ptList[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 150) * np.array([1,0])
        self.dataObj.drawFaintLine(bt1, bt2, dwg)
        bb1 = np.array(ptList[-1][0])
        bb2 =  bb1 + (self.dataObj.beam_L  + 150) * np.array([1,0])
        self.dataObj.drawFaintLine(bb1, bb2, dwg)
        #######drawing outer arrow on beam bolt group to represent pitch and end distance##########
        #pitch @ no_of_beam_bolt_row
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bb1,  str(len(pitchPts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
        #end distance
        bt2 = bt1 - self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bt2,  str(self.dataObj.edge_dist), params)          
        #end Distance
        bb2 = bb1 + self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bb1, bb2,  str(self.dataObj.edge_dist), params)
        
        # Gauge Distance when two lines of bolts present
        #Outer arrow to represent gauge 
        #faint line at top of second column bolt
        if self.dataObj.no_of_col > 1:
            A = self.BP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0])
            B = A - self.dataObj.gauge * np.array([1,0])
            offset = self.dataObj.notch_offset + 100 ##NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC
            #Faint line on second lines of bolt
            B_up = B - offset * np.array([0,1])
            self.dataObj.drawFaintLine(B,B_up, dwg) 
            params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg, A, B, str(int(self.dataObj.gauge))  , params)  

        #Faint lines and outer arrow for edge distance--RIGHT TO THE ABOVE DRAWN FAINT LINE AND OUTER ARROW
        v_offset = self.dataObj.col_T + self.dataObj.col_R1
        BR_left = self.BR - self.dataObj.end_dist * np.array([1,0])
        BR_left_up = BR_left - ((v_offset) + 180) * np.array([0,1])##NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC  
        BR_up = self.BR - ((v_offset) + 180) * np.array([0,1])##NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC     
        self.dataObj.drawFaintLine(BR_left,BR_left_up, dwg) 
        self.dataObj.drawFaintLine(self.BR,BR_up, dwg) 
        offset = ((v_offset) + 180)##NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC     
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.BR, BR_left, str(int(self.dataObj.end_dist)), params)
    ###################COLUMN CONNECTIVITY MARKING#####################
    #Draw Faint Line To Represent Distance Between Beam Flange and Cleat Angle.
        length = (self.dataObj.beam_B - self.dataObj.beam_tw)/2
        v_offset = self.dataObj.col_T + self.dataObj.col_R1 ##NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC  
        BA_down = self.BA + v_offset * np.array([0,1])
        BA_left = self.BA - 30 * np.array([1,0])
        BA_left_down = BA_left +  v_offset * np.array([0,1])
        self.dataObj.drawFaintLine(self.BA,BA_left, dwg)
        self.dataObj.drawFaintLine(self.BC1, BA_left_down, dwg)
        ##Arrow Dimension NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC  
        params = {"offset": 30, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.BA, BA_down, str(int(v_offset))  , params)
    #Draw Faint Line To Represent column pitch and end Distance.
        self.dataObj.drawFaintLine(self.BP,self.BP - (length + 30 + self.dataObj.beam_tw) * np.array([1,0]), dwg)
        self.dataObj.drawFaintLine(np.array(ptList_c[0]),np.array(ptList_c[0]) - (length + 30) * np.array([1,0]), dwg)
        offset = length + 30
        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim":10}
        BP_left = self.BP - self.dataObj.col_tw*np.array([1,0])
        self.dataObj.draw_dimension_outerArrow(dwg,BP_left, np.array(ptList_c[0]), str(int(self.dataObj.cedge_dist)) , params)
        self.dataObj.drawFaintLine(np.array(ptList_c[-1]),np.array(ptList_c[-1]) - (length + 30) * np.array([1,0]), dwg) 
        offset = length + 30
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList_c[0]), np.array(ptList_c[-1]), str(len(ptList_c) - 1) + "@" + str(int(self.dataObj.cpitch)) + ' c/c' , params)       
        self.dataObj.drawFaintLine(self.BP1,self.BP1 - (length + 30 + self.dataObj.beam_tw) * np.array([1,0]), dwg)
        offset = length + 30
        BP1_left = self.BP1 - self.dataObj.col_tw*np.array([1,0])
        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, BP1_left, np.array(ptList_c[-1]), str(int(self.dataObj.cedge_dist)) , params)        
        
###################### BEAM designation and number bolt information ##############
        # SUPORTED BEAM Designation
        beam_pt = self.BB2
        theta = 30
        offset = 50
        textUp = "Beam " + self.dataObj.beam_Designation ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
    
        # SUPORTING BEAM Designation
        theta = 45
        offset = 100
        textUp =  "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, self.BA, theta, "NW", offset, textUp,textDown)
            
        #  Secondary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
          
        bltPtx = np.array(ptList[0][0])
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8 + 75 ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)
       
        # Primary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_crows * 2* self.dataObj.no_of_ccol   
        bltPt = np.array(ptList_c[-1])
        theta = 60
        offset = (self.dataObj.beam_B/2 + 10) ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "SW", offset, textUp,textDown)        
    
        # cleat angle information
        cleatPt = self.BR1 
        theta = 75
        offset = (self.dataObj.D_beam - self.dataObj.cleat_ht - self.dataObj.notch_offset) + 100
        textUp = "ISA." + str(int(self.dataObj.cleat_legsize)) +"X" + str(int(self.dataObj.cleat_legsize_1)) +"X" + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, cleatPt, theta, "SE", offset, textUp, textDown)
        
        # 2D view name
        ptx =  self.BA + 50 * np.array([1,0]) + (v_height - 700) * np.array([0,1])
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        ## All dimensions in "mm"
        ptx =  self.BA + 400 * np.array([1,0]) + (v_height - 700) * np.array([0,1])
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        


#         dwg.add(dwg.path(d =" M0,3 C10,10 20,10 30,20", fill='black'))        
        dwg.save()
        
    def callCFBWfront(self,fileName):
        v_width = self.dataObj.D_col + 1300
        dwg = svgwrite.Drawing(fileName, size=('1200mm', '1225mm'), viewBox=('-500 -350 ' +str(v_width) + ' 1450'))
        dwg.add(dwg.polyline(points = [(self.FA),(self.FB),(self.FC),(self.FD),(self.FA)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.FE),(self.FH)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FF),(self.FG)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FC1),(self.FA1),(self.FA2),(self.FB2),(self.FB1),(self.FC2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        dwg.add(dwg.line((self.FC1),(self.FC2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FA4),(self.FA3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FB4),(self.FB3)).stroke('blue',width = 2.5,linecap = 'square'))
        
        # Weld hatching to represent WELD.
#         pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(4, 4), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
#         pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
#         dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill= "url(#diagonalHatch)", stroke='white', stroke_width=2.0))
#         

        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FW), size=(self.dataObj.cleat_legsize - self.dataObj.cleat_thk , self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        #dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.cleat_legsize, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptFP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0]) + self.dataObj.edge_dist * np.array ([0,1]) + \
                    (i-1) * self.dataObj.pitch * np.array([0,1]) + (j-1) * self.dataObj.gauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                
                ptE = pt - (bolt_r + 4) * np.array([0,1])
                PtF = pt + (bolt_r + 4) * np.array([0,1])
                dwg.add(dwg.line((ptE),(PtF)).stroke('red',width = 2.0,linecap = 'square'))
#                 ptE = self.ptFP + self.dataObj.edge_dist * np.array([1,0]) +(j-1) * self.dataObj.gauge * np.array([1,0])
#                 ptF = ptE + self.dataObj.cleat_ht * np.array([0,1])
#                 dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))   
                colList.append(pt)
            ptList.append(colList)
        
        for i in range(1,(nr_c+1)):
            pt_c = self.ptFP + self.dataObj.cedge_dist * np.array([0,1]) - self.dataObj.col_T * np.array([1,0]) + (i-1) * self.dataObj.cpitch * np.array([0,1])
            pt1_c = pt_c - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_T + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill= "black", stroke='black', stroke_width=2.0))
            pt_B1 = pt_c - 10 * np.array([1,0])
            pt_B2 = pt_c + (self.dataObj.col_T + self.dataObj.cleat_thk + 10) * np.array([1,0])
            dwg.add(dwg.line((pt_B1),(pt_B2)).stroke('black',width = 2.0,linecap = 'square'))
            ptList_c.append(pt_c)    
        
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        
                # Cross section A-A
        ptSecA = self.FA + (270 * np.array([0,-1]))
        ptSecB = ptSecA + (50 * np.array([0,1]))
        txtpt = ptSecB +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.beam_L) * np.array([1,0])
        ptSecD = ptSecC + (50 * np.array([0,1]))
        txtpt = ptSecD +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        
        
        #Included cleat height and pitch details of column bolt group
        # Drawing faint lines at right top and bottom corners of cleat--AT BEAM
        rt1 = self.FP + self.dataObj.cleat_legsize * np.array([1,0])
        rt2 = rt1 + (self.dataObj.beam_L + 225 - self.dataObj.gauge) * np.array([1,0])
        self.dataObj.drawFaintLine(rt1, rt2, dwg)
        rb1 = rt1 + self.dataObj.cleat_ht * np.array([0,1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0,1])
        self.dataObj.drawFaintLine(rb1, rb2, dwg)
        #drawing inner arrow for the above drawn faint lines
        params = {"offset": self.dataObj.beam_L , "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, rt1, rb1,  str(int(self.dataObj.cleat_ht)), params) 
        # Drawing faint lines at bolt groups on Beam
        bt1 = np.array(ptList[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 225) * np.array([1,0])
        self.dataObj.drawFaintLine(bt1, bt2, dwg)
        bb1 = np.array(ptList[-1][0])
        bb2 =  bb1 + (self.dataObj.beam_L  + 225) * np.array([1,0])
        self.dataObj.drawFaintLine(bb1, bb2, dwg)
        
        
        #drawing inner arrow beam bolt group
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bb1,  str(len(pitchPts) - 1) + "@" + str(int(self.dataObj.pitch)) + "c/c", params)
        
        bt2 = bt1 - self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bt2,  str(self.dataObj.edge_dist), params)          
        
        bb2 = bb1 + self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bb1, bb2,  str(self.dataObj.edge_dist) , params)          
                
                
        #end distance and edge distance are........DONE 
        params = {"offset": self.dataObj.D_col  + 50 , "textoffset": 145, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList_c[0]), np.array(ptList_c[-1]), str(len(ptList_c)-1)+ u' \u0040'+ str(int(self.dataObj.cpitch)) + " c/c", params)     
        
        # Distance between Beam Flange and Plate
        params = {"offset": self.dataObj.D_col + self.dataObj.gap +self.dataObj.col_T + 50, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.FA1, self.FC1,  str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params) 
        
        
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        ptOne = self.FA1
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) 
        ptTwo = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        # End Distance from the starting point of plate Information

        edgPt = self.FP - self.dataObj.col_T * np.array([1,0])
        params = {"offset": self.dataObj.D_col  + 50, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList_c[0]), edgPt,  str(int(self.dataObj.cedge_dist)), params)   
        
        # Edge Distance from plate end point.
        edgPt1 = self.FU - self.dataObj.col_T * np.array([1,0])
        params = {"offset": self.dataObj.D_col  + 50, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList_c[-1]), edgPt1,  str(int(self.dataObj.cedge_dist)), params)   
        
#         End Distance information.DO SOME ADJUSTMENTS HERE IN Y-CORDINATE
        pt1A = self.FP + self.dataObj.cleat_legsize * np.array([1,0])
        pt1B = pt1A - self.dataObj.end_dist*np.array([1,0])
        offset = self.dataObj.edge_dist + self.dataObj.beam_T + self.dataObj.beam_R1 +3
        params = {"offset": self.dataObj.D_beam/2 + self.dataObj.edge_dist - 50, "textoffset": 10, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, pt1A, pt1B, str(int(self.dataObj.end_dist)) , params)   
        
        ###Faint Lines ######
        A = self.FP + (self.dataObj.cleat_legsize ) * np.array([1,0])
        A_up = A - (self.dataObj.D_beam/2 + self.dataObj.edge_dist - 50) * np.array([0,1])
        self.dataObj.drawFaintLine(A,A_up, dwg) 
        A_left = A - self.dataObj.end_dist * np.array([1,0])
        A_left_up = A_left  - (self.dataObj.D_beam/2 + self.dataObj.edge_dist - 50) * np.array([0,1])
        self.dataObj.drawFaintLine(A_left, A_left_up, dwg) 
        
        # Gauge Distance when two lines of bolts present
        if self.dataObj.no_of_col > 1:
           
            A = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0])
            B = A - self.dataObj.gauge * np.array([1,0])
            offset = (self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + self.dataObj.edge_dist) + 50
            params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg, A, B, str(int(self.dataObj.gauge))  , params)  
            FA = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0])
            FB = FA + ((self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 130) * np.array([0,-1])
            FA_left = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist - self.dataObj.gauge) * np.array([1,0])
            FB_left = FA_left + ((self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 130) * np.array([0,-1])
#             self.dataObj.drawFaintLine(FA, FB, dwg) 
            self.dataObj.drawFaintLine(FA_left, FB_left, dwg)
        
        # Gap Distance
        gapPt = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam)/2 + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)) 
        ptG1 = self.ptFP + (gapPt + 30) * np.array([0,1])
        ptG2 = self.FC1 + (gapPt + 30) * np.array([0,1])
        offset = self.dataObj.col_L  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)
       
        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 40 * np.array([0,1])
        self.dataObj.drawFaintLine(ptC1,ptC2,dwg)
        
        ptD1 = self.FB1
        ptD2 = ptD1 + 240 * np.array([0,1])
        self.dataObj.drawFaintLine(ptD1,ptD2,dwg)
        
       
#         
        
        # The first line on the cleat for column
        ptA = self.FP
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptB = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptA, ptB, dwg)
          
        pt1 = np.array(ptList_c[0])
        ptBx = -30
        ptBy1 = ptBy + self.dataObj.cedge_dist
        pt2 = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
          
        ptOne = np.array(ptList_c[-1])
        ptBx = -30
        ptBy1 = ptBy1 + (len(ptList_c) - 1) * self.dataObj.cpitch
        ptTwo = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
          
        ptOne = self.FU
        ptBx = -30
        ptBy1 = ptBy1 + self.dataObj.cedge_dist
        ptTwo = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        
        # Beam Information
        beam_pt = self.FA1 + self.dataObj.D_beam * np.array([0,1])
        theta = 45
        offset = (self.dataObj.D_beam - self.dataObj.cleat_ht)/2 + 60.0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        
        
        
        # Column Designation
        ptx = self.dataObj.D_col /2
        pty = 0
        pt = np.array([ptx,pty])
        theta = 30
        offset = self.dataObj.col_L /10
        textUp =  "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "NW", offset, textUp,textDown)
      
        # Bolt Information for beam part
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
             
        bltPtx = np.array(ptList[0][0])
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)
        
        # Bolt Information for column part
        no_of_bolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol*2    
        bltPtx = np.array(ptList_c[-1])
        theta = 45
        offset = (self.dataObj.D_col + 10)
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "SW", offset, textUp,textDown)
        
        
        
        
        # cleat angle information
        pltPtx = self.dataObj.D_col  + self.dataObj.cleat_legsize /2
        pltPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        pltPt = np.array([pltPtx,pltPty])
        theta = 45
        offset = (self.dataObj.D_beam - self.dataObj.beam_T - self.dataObj.cleat_ht) + 50
        textUp = "ISA." + str(int(self.dataObj.cleat_legsize)) +"X" + str(int(self.dataObj.cleat_legsize_1)) +"X" + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown)
        
        
        
        # 2D view name
        ptx =  self.FA + 50 * np.array([1,0]) + 1000 * np.array([0,1]) #1150
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        ## All dimensions in "mm"
        ptx =  self.FA + 600 * np.array([1,0]) + 2000 * np.array([0,1]) #1150
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        
        dwg.save()
        
        
        
    def callCWBWfront(self,fileName):
        v_width = self.dataObj.col_B/2 + self.dataObj.gap + self.dataObj.beam_L + 1000
        dwg = svgwrite.Drawing(fileName, size=('1250mm', '1240mm'), viewBox=('-500 -400 ' +str(v_width) + ' 1500'))
        
        ptSecA = self.A + (280 * np.array([0,-1]))
        ptSecB = ptSecA + (50 * np.array([0,1]))
        txtpt = ptSecB +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = ptSecA + (self.dataObj.beam_B/2 + 30 + self.dataObj.beam_L) * np.array([1,0])
        ptSecD = ptSecC + (50 * np.array([0,1]))
        txtpt = ptSecD +(10 * np.array([-1,0])) +(80 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        
        dwg.add(dwg.polyline(points=[(self.A2),(self.B),(self.A),(self.D),(self.C) ,(self.B2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.E),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.F),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        
        # Diagonal Hatching to represent WELD
        pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(4, 4), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill= "none", stroke='blue', stroke_width=2.0))
        
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.cleat_legsize, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        #C1,A1,A3,B3,B1,C2
        dwg.add(dwg.polyline(points=[(self.C1),(self.A1),(self.A3),(self.B3),(self.B1),(self.C2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        #C1,C2
        dwg.add(dwg.line((self.C1),(self.C2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #A2,B2
        dwg.add(dwg.line((self.A2),(self.B2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.A5),(self.A4)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.B5),(self.B4)).stroke('blue',width = 2.5,linecap = 'square'))
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0]) + self.dataObj.edge_dist * np.array ([0,1]) + \
                    (i-1) * self.dataObj.pitch * np.array([0,1]) + (j-1) * self.dataObj.gauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
#                 ptE = self.ptP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1,0]) +(j-1) * self.dataObj.gauge * np.array([1,0])
#                 ptF = ptE + self.dataObj.cleat_ht * np.array([0,1])
                ptE = pt - (bolt_r + 4) * np.array([0,1])
                ptF = pt + (bolt_r + 4) * np.array([0,1])
                dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))
                colList.append(pt)
            ptList.append(colList)
        
        for i in range(1,(nr_c+1)):
            pt_c = self.ptP + self.dataObj.cedge_dist * np.array([0,1]) - self.dataObj.col_tw * np.array([1,0]) + (i-1) * self.dataObj.cpitch * np.array([0,1])
            pt1_c = pt_c - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill= "black", stroke='black', stroke_width=2.0))
            
            ptList_c.append(pt_c)
        
            
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
                
                
                
                
#     cleat Angle  Information
        pltPtx = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.cleat_legsize /2
        pltPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        pltPt = np.array([pltPtx,pltPty])
        theta = 45
        offset = (self.dataObj.D_beam + 100)/2
        textUp = "ISA. " + str(int(self.dataObj.cleat_legsize)) +"X" + str(int(self.dataObj.cleat_legsize_1)) +"X" + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown)
         
          
        # Column Designation
        ptx = self.dataObj.col_B /2
        pty = 0
        pt = np.array([ptx,pty])
        theta = 90
        offset = 100
        textUp =  "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "NW", offset, textUp,textDown)
        
        
        # Beam Information marking arrow
        beam_pt = self.B1
        theta = 60
        offset =  250
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
         
        # beam Bolt Information arrow
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        bltPtx = np.array(ptList[0][0])
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = str(no_of_bolts) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)

      
       # column bolt marking Arrow
        no_of_cbolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        theta = 45
        offset = (self.dataObj.col_B *3)/4
        textUp = str(no_of_cbolts) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'  
        self.dataObj.drawOrientedArrow(dwg, np.array(ptList_c[0]), theta, "NW", offset, textUp, textDown) 
        
        
        #Included cleat height and pitch details of column bolt group
        # Drawing faint lines at right top and bottom corners of cleat--AT BEAM
        rt1 = self.P + self.dataObj.cleat_legsize * np.array([1,0])
        rt2 = rt1 + (self.dataObj.beam_L + 275 - self.dataObj.gauge) * np.array([1,0])
        self.dataObj.drawFaintLine(rt1, rt2, dwg)
        rb1 = rt1 + self.dataObj.cleat_ht * np.array([0,1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0,1])
        self.dataObj.drawFaintLine(rb1, rb2, dwg)
        #drawing inner arrow for the above drawn faint lines
        params = {"offset": self.dataObj.beam_L , "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, rt1, rb1,  str(int(self.dataObj.cleat_ht)), params) 
        # Drawing faint lines at bolt groups on column
        bt1 = np.array(ptList[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 275) * np.array([1,0])
        self.dataObj.drawFaintLine(bt1, bt2, dwg)
        bb1 = np.array(ptList[-1][0])
        bb2 =  bb1 + (self.dataObj.beam_L  + 275) * np.array([1,0])
        self.dataObj.drawFaintLine(bb1, bb2, dwg)
        #drawing outer arrow beam bolt group
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bb1,  str(len(ptList) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
        
        bt2 = bt1 - self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt1, bt2,  str(self.dataObj.edge_dist), params)          
        
        bb2 = bb1 + self.dataObj.edge_dist * np.array([0,1])  
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bb1, bb2,  str(self.dataObj.edge_dist), params)
        
        ####Column bolt group and related dimension marking
        # The first line on the cleat for column
        ptA = self.P
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptB = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptA, ptB, dwg)
        #Faint lines for column bolt group and edge distances  
        pt1 = np.array(ptList_c[0])
        ptBx = -30
        ptBy1 = ptBy + self.dataObj.cedge_dist
        pt2 = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
          
        ptOne = np.array(ptList_c[-1])
        ptBx = -30
        ptBy1 = ptBy1 + (len(ptList_c) - 1) * self.dataObj.cpitch
        ptTwo = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
          
        ptOne = self.U
        ptBx = -30
        ptBy1 = ptBy1 + self.dataObj.cedge_dist
        ptTwo = (ptBx,ptBy1)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        #Outer arrow for the pitch,edge distance marking
        #Related to the above drawn faint line
        #drawing inner arrow beam bolt group
        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw)/2 + 30 , "textoffset": 150, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList_c[0]), ptList_c[-1],  str(len(ptList_c) - 1) + "@" + str(int(self.dataObj.cpitch))+ " c/c", params)
        
        bt2 = self.P - self.dataObj.col_tw * np.array([1,0]) 
        params = {"offset":(self.dataObj.col_B - self.dataObj.col_tw)/2 + 30, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, bt2, np.array(ptList_c[0]),  str(int(self.dataObj.cedge_dist)) , params)          
         
          
        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw)/2 + 30, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptList_c[-1], self.P + self.dataObj.cleat_ht * np.array([0,1]) - self.dataObj.col_tw,  str(int(self.dataObj.cedge_dist)) , params) 
        
        # faint lines and outer arrow for the edge distance--AT BEAM
        rt = self.P + self.dataObj.cleat_legsize * np.array([1,0])
        rt1 = rt - (self.dataObj.beam_T + self.dataObj.beam_R1 +130) * np.array([0,1])
        rt_left = rt - self.dataObj.end_dist * np.array([1,0])
        rt_left_top = rt_left - (self.dataObj.beam_T + self.dataObj.beam_R1 +130) * np.array([0,1]) 
        self.dataObj.drawFaintLine(rt, rt1, dwg)
        self.dataObj.drawFaintLine(rt_left, rt_left_top, dwg)
        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw)/2 + 60, "textoffset": 10, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, rt, rt_left,  str(int(self.dataObj.end_dist)) , params) 
        # faint lines and outer arrow for beam gauge representation for double lines of bolts
        if self.dataObj.no_of_col > 1:    
            rt_left_left = rt_left - self.dataObj.gauge * np.array([1,0]) #make center line of bolts
            rt_left_left_top = rt_left_left - (self.dataObj.beam_T + self.dataObj.beam_R1 +130) * np.array([0,1])
            self.dataObj.drawFaintLine(rt_left_left, rt_left_left_top, dwg)
            params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw)/2 + 15, "textoffset": 10, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg, rt_left, rt_left_left,  str(int(self.dataObj.gauge)), params) 
        
        # 2D view name
        ptx =  self.A + 50 * np.array([1,0]) + 1010 * np.array([0,1]) #1090
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        ## All dimensions in "mm"
        ptx2 =  ptx + 250 * np.array([1,0])
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx2), fill='black',font_family = "sans-serif",font_size = 30))      
        dwg.save()
        
    
             
class cleat2DCreatorTop(object):
    
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        self.A = np.array([0,0])
        self.B = np.array([0,0]) + (self.dataObj.col_B)* np.array([1,0])
        self.C = self.B + (self.dataObj.col_T)* np.array([0,1])
        self.D = self.A +  (self.dataObj.col_B + self.dataObj.col_tw)/2 * np.array([1,0]) + (self.dataObj.col_T) * np.array([0,1])
        self.E = self.A +  (self.dataObj.col_B + self.dataObj.col_tw)/2 * np.array([1,0]) + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.F = self.B + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.G = self.B + (self.dataObj.D_col)* np.array([0,1])
        self.H = self.A + (self.dataObj.D_col)* np.array([0,1])
        self.I = self.A + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.J = self.E - (self.dataObj.col_tw) * np.array([1,0])
        self.K = self.D - (self.dataObj.col_tw) * np.array([1,0])
        self.L = self.A + (self.dataObj.col_T)* np.array([0,1])
        self.A7 = self.A + (self.dataObj.col_B/2 + self.dataObj.col_tw/2 + self.dataObj.gap) * np.array([1,0]) + (self.dataObj.D_col/2 - self.dataObj.beam_tw/2) * np.array([0,1])

        self.A1 = self.A7 + (self.dataObj.beam_B/2 - self.dataObj.beam_tw/2) * np.array([0,-1])
        self.A4 = self.A1 + self.dataObj.beam_B * np.array([0,1])
        self.A5 = self.A7 - 20 * np.array([1,0])
        self.A8 = self.A7 + (self.dataObj.beam_L) * np.array([1,0])
        self.P1 = self.A1 + (self.dataObj.beam_B + self.dataObj.beam_tw) /2 * np.array([0,1])
        self.A6 = self.P1 + (self.dataObj.beam_L) * np.array([1,0])
        self.P = self.P1 - 20 * np.array([1,0])
        self.P2 = self.P + (self.dataObj.cleat_legsize) * np.array([1,0])
        self.P3 = self.P2 + (self.dataObj.cleat_thk)* np.array([0,1])
        self.P6 = self.P3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk)*np.array([1,0])
        self.P5 = self.P6 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk)* np.array([0,1])
        self.P4 = self.P5 - (self.dataObj.cleat_thk)* np.array([1,0])
        self.P7 = self.P1 + (self.dataObj.cleat_thk)* np.array([0,1])
        self.Q = self.P1 - 20 * np.array([1,0])-(self.dataObj.beam_tw)*np.array([0,1])
        self.Q1 = self.Q + (self.dataObj.gap) * np.array([1,0])  
        self.Q2 = self.Q + (self.dataObj.cleat_legsize)* np.array([1,0])
        self.Q3 = self.Q2 - (self.dataObj.cleat_thk)*np.array([0,1])
        self.Q7 = self.Q1 -(self.dataObj.cleat_thk)*np.array([0,1])
        self.Q6 = self.Q3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk)* np.array([1,0])
        self.Q5 = self.Q6 - (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk)*np.array([0,1])
        self.Q4 = self.Q5 - (self.dataObj.cleat_thk)* np.array([1,0])
        

        
        # Weld Triangle
        
        self.ptP = self.P + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.O = self.P + self.dataObj.cleat_thk * np.array([1,0])
        self.ptO = self.O  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.R = self.P + self.dataObj.cleat_thk * np.array([0,-1])
        self.ptR = self.R + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1]) 
        
        self.X = self.P + (self.dataObj.cleat_thk)* np.array([0,1])
        self.ptX = self.X + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.Y = self.X + (self.dataObj.cleat_thk) * np.array([0,1])
        self.ptY = self.Y + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.Z = self.X + (self.dataObj.cleat_thk) * np.array([1,0])
        self.ptZ = self.Z + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        
        
        #### CFBW connectivity points
        self.FA = np.array([0,0])
        self.FB = self.FA + self.dataObj.col_T * np.array([1,0])
        self.FC = self.FB + (self.dataObj.col_B - self.dataObj.col_tw)/2 * np.array([0,1])
        self.FD = self.FC  + (self.dataObj.D_col - 2*(self.dataObj.col_T))* np.array([1,0])
        self.FE = self.FA + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1,0])
        self.FF = self.FA + self.dataObj.D_col * np.array([1,0])
        self.FG = self.FF + self.dataObj.col_B * np.array([0,1])
        self.FH = self.FG + self.dataObj.col_T * np.array([-1,0])
        self.FI = self.FD + self.dataObj.col_tw * np.array([0,1])
        self.FJ = self.FC + self.dataObj.col_tw * np.array([0,1])
        self.FK = self.FB + self.dataObj.col_B * np.array([0,1])
        self.FL = self.FK + self.dataObj.col_T * np.array([-1,0])
#         self.FA7 = self.FD + (self.dataObj.col_T + self.dataObj.gap) * np.array([1,0])
#         self.FP1 = self.FA7 + self.dataObj.beam_tw * np.array([0,1])
#         self.FP = self.FP1 + self.dataObj.gap * np.array([-1,0])
#         self.FA1 = self.FA7 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 *np.array([0,-1])
#         self.FA2 = self.FA1 + self.dataObj.beam_L * np.array([1,0])
#         self.FA3 = self.FA2 + self.dataObj.beam_B * np.array([0,1])
#         self.FA4 = self.FA1 + self.dataObj.beam_B * np.array([0,1])
#         self.FX = self.FP + self.dataObj.cleat_thk * np.array([0,1])
#         self.FP2 = self.FP + self.dataObj.cleat_legsize * np.array([1,0])
#         self.FP3 = self.FP2 + self.dataObj.cleat_thk * np.array([0,1])
#         self.FP4 =  self.FX + self.dataObj.gap * np.array([1,0])
#         self.FA8 = self.FA7 + self.dataObj.beam_L * np.array([1,0])
#         self.FA6 = self.FP1 + self.dataObj.beam_L * np.array([1,0])
#         self.FP5 = self.FA7 + self.dataObj.gap * np.array([-1,0])
        
        self.FA7 = self.FA + (self.dataObj.D_col + self.dataObj.gap) * np.array([1,0]) + (self.dataObj.col_B/2 - self.dataObj.beam_tw/2) * np.array([0,1])

        self.FA1 = self.FA7 + (self.dataObj.beam_B/2 - self.dataObj.beam_tw/2) * np.array([0,-1])
        self.FA4 = self.FA1 + self.dataObj.beam_B * np.array([0,1])
        self.FA5 = self.FA7 - 20 * np.array([1,0])
        self.FA8 = self.FA7 + (self.dataObj.beam_L) * np.array([1,0])
        self.FP1 = self.FA1 + (self.dataObj.beam_B + self.dataObj.beam_tw) /2 * np.array([0,1])
        self.FA6 = self.FP1 + (self.dataObj.beam_L) * np.array([1,0])
        self.FP = self.FP1 - 20 * np.array([1,0])
        self.FP2 = self.FP + (self.dataObj.cleat_legsize) * np.array([1,0])
        self.FP3 = self.FP2 + (self.dataObj.cleat_thk)* np.array([0,1])
        self.FP6 = self.FP3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk)*np.array([1,0])
        self.FP5 = self.FP6 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk)* np.array([0,1])
        self.FP4 = self.FP5 - (self.dataObj.cleat_thk)* np.array([1,0])
        self.FP7 = self.FP1 + (self.dataObj.cleat_thk)* np.array([0,1])
        self.FQN = self.FP1 - 20 * np.array([1,0])-(self.dataObj.beam_tw)*np.array([0,1])
        self.FQ1 = self.FQN + (self.dataObj.gap) * np.array([1,0])  
        self.FQ2 = self.FQN + (self.dataObj.cleat_legsize)* np.array([1,0])
        self.FQ3 = self.FQ2 - (self.dataObj.cleat_thk)*np.array([0,1])
        self.FQ7 = self.FQ1 -(self.dataObj.cleat_thk)*np.array([0,1])
        self.FQ6 = self.FQ3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk)* np.array([1,0])
        self.FQ5 = self.FQ6 - (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk)*np.array([0,1])
        self.FQ4 = self.FQ5 - (self.dataObj.cleat_thk)* np.array([1,0])
#         # Weld Triangle
#         
#         self.ptFP = self.FP + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
#         self.FQ = self.FP + self.dataObj.cleat_thk * np.array([1,0])
#         self.ptFQ = self.FQ  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
#         self.FR = self.FP + self.dataObj.cleat_thk * np.array([0,-1])
#         self.ptFR = self.FR + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1]) 
#         
#         self.FX = self.FP + (self.dataObj.cleat_thk)* np.array([0,1])
#         self.ptFX = self.FX + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
#         self.FY = self.FX + (self.dataObj.cleat_thk) * np.array([0,1])
#         self.ptFY = self.FY + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
#         self.FZ = self.FX + (self.dataObj.cleat_thk) * np.array([1,0])
#         self.ptFZ = self.FZ + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        
        # Points for Beam - Beam connection
        self.beam_beam_length = self.dataObj.beam_B + 200
        # for primary beam
        self.notch_length  = (self.dataObj.col_B - self.dataObj.col_tw)/2 -10
        
        self.BA = (0,0)
        self.BB = self.BA + (self.dataObj.col_B) * np.array([1,0])
        self.BC = self.BB + self.beam_beam_length * np.array([0,1])
        self.BD = self.BA + self.beam_beam_length * np.array([0,1])
        self.BE = self.BA + (self.dataObj.col_B -self.dataObj.col_tw)/2 * np.array([1,0])
        self.BF = self.BE + self.beam_beam_length * np.array([0,1])
        self.BG = self.BE + self.dataObj.col_tw * np.array([1,0])
        self.BH = self.BG + self.beam_beam_length * np.array([0,1])
        
        # for secondary beam
        
        self.BA3 = self.BB + 10 * np.array([1,0]) + (self.beam_beam_length - self.dataObj.beam_B)/2 * np.array([0,1]) 
        self.BA2 = self.BA3 - 10*np.array([1,0])
        self.BA1 = self.BA3 - self.notch_length * np.array([1,0])
        self.BA4 = self.BA3 + (self.dataObj.beam_L-self.notch_length) * np.array([1,0])
        self.BA5 = self.BA4 + self.dataObj.beam_B * np.array([0,1])
        self.BA6 = self.BA3 + self.dataObj.beam_B * np.array([0,1])
        self.BA7 = self.BA2 + self.dataObj.beam_B * np.array([0,1])
        self.BA8 = self.BA1 + self.dataObj.beam_B * np.array([0,1])
        self.BA9 = self.BA1 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA10 = self.BA2 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA11 = self.BA3 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA12 = self.BA4 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA13 = self.BA4 + (self.dataObj.beam_B + self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA14 = self.BA3 + (self.dataObj.beam_B + self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA15 = self.BA2 + (self.dataObj.beam_B + self.dataObj.beam_tw)/2 * np.array([0,1])
        self.BA16 = self.BA1 + (self.dataObj.beam_B + self.dataObj.beam_tw)/2 * np.array([0,1])
        
        
        

#          for cleat angle 
        self.BP1 = self.BG + (self.beam_beam_length/2 - self.dataObj.beam_tw/2 - self.dataObj.cleat_legsize_1) * np.array([0,1]) # BEAM_TW
        self.BP2 = self.BP1 + self.dataObj.cleat_thk * np.array([1,0])
        self.BP3 = self.BP2 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0,1])
        self.BP4 = self.BB + (self.beam_beam_length/2 - self.dataObj.beam_tw/2 - self.dataObj.cleat_thk) * np.array([0,1]) # BEAM_TW
        self.BP5 = self.BP4 + 10*np.array([1,0])
        self.BP6 = self.BP3 + (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1,0])
        self.BP7 = self.BP6 + self.dataObj.cleat_thk * np.array([0,1])
        self.BP9 = self.BP4 + self.dataObj.cleat_thk * np.array([0,1])
        self.BP10 = self.BP1 + self.dataObj.cleat_legsize_1 * np.array([0,1])
         
         
        self.BQ1 = self.BH + (self.beam_beam_length/2 - self.dataObj.beam_tw/2 - self.dataObj.cleat_legsize_1) * np.array([0,-1]) # BEAM_TW
        self.BQ2 = self.BQ1 + self.dataObj.cleat_thk * np.array([1,0])
        self.BQ3 = self.BQ2 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0,-1])
        self.BQ4 = self.BC + (self.beam_beam_length/2 - self.dataObj.beam_tw/2 - self.dataObj.cleat_thk) * np.array([0,-1]) # BEAM_TW
        self.BQ5 = self.BQ4 + 10*np.array([1,0])
        self.BQ6 = self.BQ3 + (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1,0])
        self.BQ7 = self.BQ6 + self.dataObj.cleat_thk * np.array([0,-1])
        self.BQ9 = self.BQ4 + self.dataObj.cleat_thk * np.array([0,-1])
        self.BQ10 = self.BQ1 + self.dataObj.cleat_legsize_1 * np.array([0,-1])
        
    def callBWBWTop(self,fileName):
        
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-200 -250 1200 900'))
        
        ############ B-B section #################
        ptSecA = self.BB + ((300+ self.dataObj.gap + self.dataObj.beam_L) * np.array([1,0]))
        ptSecB = ptSecA + (50 * np.array([-1,0]))
        txtpt = ptSecB +(80 * np.array([-1,0])) +(20 * np.array([0,1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = self.BC + ((300 + self.dataObj.gap + self.dataObj.beam_L) * np.array([1,0]))
        ptSecD = ptSecC + (50 * np.array([-1,0]))
        txtpt = ptSecD +(80 * np.array([-1,0])) +(20 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
         
        ############ C-C section #################
        ptSecA = self.FL + (50)*np.array([-1,0]) + ((self.dataObj.D_beam * 3)/8 +125)*np.array([0,1])
        ptSecB = ptSecA + (50 * np.array([0,-1]))
        txtpt = ptSecB +(20 * np.array([-1,0])) +(40 * np.array([0,-1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = ptSecA + (self.dataObj.col_B+self.dataObj.gap+self.dataObj.beam_L + 50)*np.array([1,0])
        ptSecD = ptSecC + (50 * np.array([0,-1]))
        txtpt = ptSecD +(20 * np.array([-1,0])) +(40 * np.array([0,-1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.BA),(self.BB),(self.BC),(self.BD),(self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BE),(self.BF)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.BG),(self.BH)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.BA2),(self.BA1),(self.BA8),(self.BA7)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        
#         dwg.add(dwg.line((self.BA2),(self.BA1),(self.BA8),(self.BA7)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        
        
        dwg.add(dwg.polyline(points=[(self.BA2),(self.BA1),(self.BA8),(self.BA7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))

        dwg.add(dwg.polyline(points=[(self.BA2),(self.BA3),(self.BA4),(self.BA5),(self.BA6),(self.BA7)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BA3),(self.BA6)).stroke('blue',width = 2.5,linecap = 'square'))
        
        
        dwg.add(dwg.line((self.BA9),(self.BA10)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.BA16),(self.BA15)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))


        dwg.add(dwg.line((self.BA10),(self.BA11)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.BA15),(self.BA14)).stroke('blue',width = 2.5,linecap = 'square'))
        
        dwg.add(dwg.line((self.BA11),(self.BA12)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.BA14),(self.BA13)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #cleat Angle 
        dwg.add(dwg.polyline(points=[(self.BP1),(self.BP2),(self.BP3),(self.BP6),(self.BP7),(self.BP10),(self.BP1)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.BQ1),(self.BQ2),(self.BQ3),(self.BQ6),(self.BQ7),(self.BQ10),(self.BQ1)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))


#         dwg.add(dwg.line((self.BH1),(self.BG1)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.BE1),(self.BF1)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.polyline(points=[(self.BJ1),(self.BI1),(self.BL1),(self.BK1),(self.BA)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.BP4),(self.BP5)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.line((self.BP9),(self.BG1)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.line((self.BQ9),(self.BE1)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.line((self.BQ4),(self.BQ5)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.polyline(points=[(self.BP9),(self.BP10),(self.BP1),(self.BP2),(self.BP3),(self.BP4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.polyline(points=[(self.BQ9),(self.BQ10),(self.BQ1),(self.BQ2),(self.BQ3),(self.BQ4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.BP10 + self.dataObj.gap * np.array([1,0])),(self.BQ10 + self.dataObj.gap * np.array([1,0]))).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))

        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []
        ptList_c_1 = []
        if nc >= 1:
            for col in range (nc):
                pt = self.BP6  - self.dataObj.end_dist * np.array([1,0]) - (col) * self.dataObj.gauge * np.array([1,0])
                pt1 = pt - bolt_r *  np.array([1,0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2*(self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0,-1])
                B2 = pt + (rect_ht + 10) * np.array([0,1])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList.append(pt)
#                 if len(ptList) > 1:
#                     dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 100
#                     pt1  = np.array(ptList[1])
#                     pt2 = pt1 - (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 100) * np.array([0,1])
# #                     self.dataObj.drawFaintLine(pt1,pt2,dwg)
#                     params = {"offset": dimOffset, "textoffset": 20, "lineori": "right", "endlinedim":10}
#                     self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),np.array(ptList[1]),  str(int(self.dataObj.gauge)) + "mm", params)  
#                     self.dataObj.drawFaintLine(pt1,pt2,dwg)
        if nc_c >= 1:
            for col in range (nc_c): 
                pt_c = self.BP1  + self.dataObj.cend_dist * np.array([0,1]) - self.dataObj.col_tw *np.array([1,0]) + (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c = pt_c - bolt_r *  np.array([0,1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1,0])
                B2 = pt_c + (rect_length + 10) * np.array([1,0])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList_c.append(pt_c)
                
                
                pt_c1 = self.BQ1  + self.dataObj.cend_dist * np.array([0,-1]) - self.dataObj.col_tw *np.array([1,0]) - (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c1 = pt_c1 - bolt_r *  np.array([0,1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1),fill = 'black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1,0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1,0])
                dwg.add(dwg.line((B1_1),(B2_1)).stroke('black',width = 2.5,linecap = 'square'))
                ptList_c_1.append(pt_c1)        
        
        #Faint lines and outer arrow for column cleat connectivity
        #Faint lines at the edge of the plate
        #above the beam part
        pt2 = self.BP1- (self.dataObj.col_B + 200+ self.dataObj.col_T)/2 * np.array([1,0])
        self.dataObj.drawFaintLine(self.BP1,pt2,dwg)
        ptx = np.array(ptList_c[0]) - (self.dataObj.col_B + 200)/2 * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c[0]),ptx,dwg)
        pt2_left = self.BP1 - self.dataObj.col_tw * np.array([1,0])
        params = {"offset": (self.dataObj.col_B + 200)/2 , "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt2_left,np.array(ptList_c[0]),  str(int(self.dataObj.cend_dist)) , params)  
        #below the beam part
        pt2 = self.BQ1- (self.dataObj.col_B + 200+ self.dataObj.col_T)/2 * np.array([1,0])
        self.dataObj.drawFaintLine(self.BQ1,pt2,dwg)
        ptx = np.array(ptList_c_1[0]) - (self.dataObj.col_B + 200)/2 * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c_1[0]),ptx,dwg)
        pt2_left = self.BQ1 - self.dataObj.col_tw * np.array([1,0])
        params = {"offset": (self.dataObj.col_B + 200)/2 , "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt2_left,np.array(ptList_c_1[0]),  str(int(self.dataObj.cend_dist)) , params)  
        if nc_c > 1:
            pt1 = np.array(ptList_c[1])
            pt2 = pt1 - (self.dataObj.col_B + 200)/2 * np.array([1,0])
            self.dataObj.drawFaintLine(pt1,pt2,dwg)
            params = {"offset": (self.dataObj.col_B + 200)/2 , "textoffset": 50, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt1,np.array(ptList_c[0]),  str(int(self.dataObj.cgauge)) , params)  
        
            pt1 = np.array(ptList_c_1[1])
            pt2 = pt1 - (self.dataObj.col_B + 200)/2 * np.array([1,0])
            self.dataObj.drawFaintLine(pt1,pt2,dwg)
            params = {"offset": (self.dataObj.col_B + 200)/2 , "textoffset": 50, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt1,np.array(ptList_c_1[0]),  str(int(self.dataObj.cgauge)) , params)  
        
        #marking and drawing arrow for beam connectivity
        dimOffset = self.beam_beam_length/2 + 25
        pt1 = np.array(ptList[0])
        pt2 = self.BP6
        pt3 = pt1 - dimOffset * np.array([0,1])
        pt4 = pt2 - dimOffset * np.array([0,1])
        self.dataObj.drawFaintLine(pt1,pt3,dwg)
        self.dataObj.drawFaintLine(pt2,pt4,dwg)
        params = {"offset": dimOffset , "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt1,pt2,  str(int(self.dataObj.end_dist)) , params)
        if nc > 1:
            pt1 = np.array(ptList[1])
            pt2 = pt1 - dimOffset * np.array([0,1]) 
            self.dataObj.drawFaintLine(pt1,pt2,dwg)
            params = {"offset": dimOffset + 25 , "textoffset": 10, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt1,np.array(ptList[0]),  str(int(self.dataObj.gauge)) , params)
#########################All Dimensional marking has been done ######################
       
     # Beam Information
        beam_pt = (self.BA4 + self.BA5)/2
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
         
        # Column Information
        col_pt = (self.BA + self.BB)/2
        theta = 90
        offset = 150
        textUp = "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NE", offset, textUp, textDown)
         
        # cleat information
        plt_pt = self.BP6 
        theta = 40
        offset =  self.dataObj.beam_B /2 + 50
        textUp = "ISA. " + str(int(self.dataObj.cleat_legsize))+'x'+ str(int(self.dataObj.cleat_legsize_1))+ 'x' + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "NE", offset, textUp, textDown)
         
        # Bolt Information for beam connectivity
#         bltPt = self.FP5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0]) 
        bltPt = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.beam_B) + 100
        textUp = str(self.dataObj.no_of_rows * self.dataObj.no_of_col) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp,textDown)
         
        # Bolt information for column connectivity
        no_of_bolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2  
        weldPt = np.array(ptList_c_1[-1])
        theta = 30
        offset =  (self.beam_beam_length -  2 * self.dataObj.cleat_legsize) /2  + 25
        textUp = str(no_of_bolts) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "SE", offset, textUp, textDown)
        # Gap Informatoin
        ptG1 = self.BC + 100 * np.array([0,1])
        ptG2 = ptG1 + 20 * np.array([1,0])
        offset = 1
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)
        # Draw Faint Lines to representation of Gap distance 
        ptA = self.BC
        ptB = ptG1
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.BA6
        ptD = ptC + (self.dataObj.D_col - self.dataObj.beam_B)/2 * np.array([0,1])
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
        
        # 2D view name
        ptx =  self.FA + (150)* np.array([1,0]) + (640)*np.array([0,1]) #640
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30)) 
        ptx =  ptx + 350 * np.array([1,0]) 
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        
        
        dwg.save()
        dwg.save()
        

    def callCFBWTop(self,fileName):
        '''
        '''
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-300 -250 1500 1000'))
        
        ############ B-B section #################
        ptSecA = self.FF + ((290+ self.dataObj.gap + self.dataObj.beam_L) * np.array([1,0]))
        ptSecB = ptSecA + (50 * np.array([-1,0]))
        txtpt = ptSecB +(80 * np.array([-1,0])) +(20 * np.array([0,1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = self.FG + ((290+ self.dataObj.gap + self.dataObj.beam_L) * np.array([1,0]))
        ptSecD = ptSecC + (50 * np.array([-1,0]))
        txtpt = ptSecD +(80 * np.array([-1,0])) +(20 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
         
        ############ C-C section #################
        ptSecA = self.FL + (50)*np.array([-1,0]) + ((self.dataObj.D_beam * 3)/8 +100)*np.array([0,1])
        ptSecB = ptSecA + (50 * np.array([0,-1]))
        txtpt = ptSecB +(20 * np.array([-1,0])) +(40 * np.array([0,-1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = ptSecA + (self.dataObj.D_col+self.dataObj.gap+self.dataObj.beam_L + 100)*np.array([1,0])
        ptSecD = ptSecC + (50 * np.array([0,-1]))
        txtpt = ptSecD +(20 * np.array([-1,0])) +(40 * np.array([0,-1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        
        dwg.add(dwg.polyline(points=[(self.FA),(self.FB),(self.FC),(self.FD),(self.FE),(self.FF),(self.FG),(self.FH),(self.FI),(self.FJ),(self.FK),(self.FL),(self.FA)], stroke='blue', fill='none', stroke_width=2.5))
#         dwg.add(dwg.rect(insert=(self.FA1), size=(self.dataObj.beam_L, self.dataObj.beam_B),fill = 'none', stroke='blue', stroke_width=2.5))
#         dwg.add(dwg.line((self.FP),(self.FP1)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.line((self.FX),(self.FP4)).stroke('blue',width = 2.5,linecap = 'square'))
#         dwg.add(dwg.polyline(points=[(self.FP1),(self.FP2),(self.FP3),(self.FP4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.FA7),(self.FA8)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.line((self.FP1),(self.FA6)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
#         dwg.add(dwg.polyline([(self.ptFP), (self.ptFQ), (self.ptFR), (self.ptFP)], fill='black',stroke_width=2.5,stroke='black'))
#         dwg.add(dwg.polyline([(self.ptFX), (self.ptFY), (self.ptFZ), (self.ptFX)], fill='black',stroke_width=2.5,stroke='black'))
        
        dwg.add(dwg.rect(insert=(self.FA1), size=(self.dataObj.beam_L, self.dataObj.beam_B),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.FA7),(self.FA8)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FP1),(self.FA6)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FP),(self.FP1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FP1),(self.FP2),(self.FP3),(self.FP7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.FP7),(self.FP6),(self.FP5),(self.FP4)], stroke='blue', fill='none', stroke_width=2.5))
        
        dwg.add(dwg.line((self.FQN),(self.FQ1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FQ1),(self.FQ2),(self.FQ3),(self.FQ7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.FQ7),(self.FQ6),(self.FQ5),(self.FQ4)], stroke='blue', fill='none', stroke_width=2.5))

        
        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []
        ptList_c_1 = []
        if nc >= 1:
            for col in range (nc):
                pt = self.FQ3  - self.dataObj.end_dist * np.array([1,0]) - (col) * self.dataObj.gauge * np.array([1,0])
                pt1 = pt - bolt_r *  np.array([1,0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2*(self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0,-1])
                B2 = pt + (rect_ht + 10) * np.array([0,1])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList.append(pt)
                if len(ptList) > 1:
                    dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 100
                    pt1  = np.array(ptList[1])
                    pt2 = pt1 - (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 100) * np.array([0,1])
#                     self.dataObj.drawFaintLine(pt1,pt2,dwg)
                    params = {"offset": dimOffset, "textoffset": 20, "lineori": "right", "endlinedim":10}
                    self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),np.array(ptList[1]),  str(int(self.dataObj.gauge)), params)  
                    self.dataObj.drawFaintLine(pt1,pt2,dwg)
        if nc_c >= 1:
            for col in range (nc_c): 
                pt_c = self.FQ4  + self.dataObj.cend_dist * np.array([0,1]) - self.dataObj.col_T *np.array([1,0]) + (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c = pt_c - bolt_r *  np.array([0,1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1,0])
                B2 = pt_c + (rect_length + 10) * np.array([1,0])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList_c.append(pt_c)
                
                
                pt_c1 = self.FP4  + self.dataObj.cend_dist * np.array([0,-1]) - self.dataObj.col_T*np.array([1,0]) - (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c1 = pt_c1 - bolt_r *  np.array([0,1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_T + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1),fill = 'black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1,0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1,0])
                dwg.add(dwg.line((B1_1),(B2_1)).stroke('black',width = 2.5,linecap = 'square'))
                ptList_c_1.append(pt_c1)
        
#                 if len(ptList_c) > 1:
#                     dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 50
#                     params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim":10}
#                     self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),np.array(ptList_c[1]),  str(int(self.dataObj.gauge)) , params)  
        
        if nc_c > 1:     
            ptb = np.array(ptList_c[1])
            ptb1 = ptb - (self.dataObj.D_col + 30)*np.array([1,0])
            params = {"offset": self.dataObj.D_col + 30 , "textoffset": 100, "lineori": "right", "endlinedim":10}
#             self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),np.array(ptList_c[1]),  str(int(self.dataObj.gauge)) , params)  
            self.dataObj.drawFaintLine(ptb,ptb1,dwg)
            self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),np.array(ptList_c[1]),  str(int(self.dataObj.cgauge)) , params)  

             
            ptb = np.array(ptList_c_1[1])
            ptb1 = ptb - (self.dataObj.D_col + 30)*np.array([1,0])
            params = {"offset": self.dataObj.D_col + 30 , "textoffset": 100, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c_1[0]),np.array(ptList_c_1[1]),  str(int(self.dataObj.cgauge)) , params)  
            self.dataObj.drawFaintLine(ptb,ptb1,dwg)


        #Faint lines and outer arrow for column cleat connectivity
        #Faint lines at the edge of the plate
        #above the beam part
        pt2 = self.FQ4- (self.dataObj.D_col + 30+ self.dataObj.col_T) * np.array([1,0])
        self.dataObj.drawFaintLine(self.FQ4,pt2,dwg)
        ptx = np.array(ptList_c[0]) - (self.dataObj.D_col + 30) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c[0]),ptx,dwg)
        pt2_left = self.FQ4 - self.dataObj.col_T * np.array([1,0])
        params = {"offset": self.dataObj.D_col + 30 , "textoffset": 100, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt2_left,np.array(ptList_c[0]),  str(int(self.dataObj.cend_dist)) , params)  
        #below the beam part
        pt2 = self.FP4- (self.dataObj.D_col + 30+ self.dataObj.col_T) * np.array([1,0])
        self.dataObj.drawFaintLine(self.FP4,pt2,dwg)
        ptx = np.array(ptList_c_1[0]) - (self.dataObj.D_col + 30) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c_1[0]),ptx,dwg)
        pt2_left = self.FP4 - self.dataObj.col_T * np.array([1,0])
        params = {"offset": self.dataObj.D_col + 30 , "textoffset": 100, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt2_left,np.array(ptList_c_1[0]),  str(int(self.dataObj.cend_dist)) , params)  
        #marking and drawing arrow for beam connectivity
        dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 150
        pt1 = np.array(ptList[0])
        pt2 = self.FQ3
        pt3 = pt1 - dimOffset * np.array([0,1])
        pt4 = pt2 - dimOffset * np.array([0,1])
        self.dataObj.drawFaintLine(pt1,pt3,dwg)
        self.dataObj.drawFaintLine(pt2,pt4,dwg)
        params = {"offset": dimOffset , "textoffset": 10, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,pt1,pt2,  str(int(self.dataObj.end_dist)) , params) 
#########################All Dimensional marking has been done ######################
       
     # Beam Information
        beam_pt = self.FA6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
         
        # Column Information
        col_pt = self.FL
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown)
         
        # cleat information
        plt_pt = self.FP3 
        theta = 45
        offset =  self.dataObj.beam_B /2 + 50
        textUp = "ISA. " + str(int(self.dataObj.cleat_legsize))+'x'+ str(int(self.dataObj.cleat_legsize_1))+ 'x' + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown)
         
        # Bolt Information for beam connectivity
#         bltPt = self.FP5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0]) 
        bltPt = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.beam_B) + 50
        textUp = str(self.dataObj.no_of_rows*self.dataObj.no_of_col) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp,textDown)
         
        # Bolt information for column connectivity
        no_of_bolts = self.dataObj.no_of_crows * 2 *self.dataObj.no_of_ccol  
        weldPt = np.array(ptList_c[0])
        theta = 40
        offset =  (self.dataObj.D_col -  self.dataObj.beam_B) /2 + 80
        textUp = str(no_of_bolts) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown)
        # Gap Informatoin
        ptG1 = self.FG + 50 * np.array([0,1])
        ptG2 = ptG1 + 20 * np.array([1,0])
        offset = 1
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
        # Draw Faint Lines to representation of Gap distance 
        ptA = self.FG
        ptB = ptG1
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.FA4
        ptD = ptC + (self.dataObj.D_col - self.dataObj.beam_B)/2 * np.array([0,1])
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
        
        # 2D view name
        ptx =  self.FA + (250)* np.array([1,0]) + (740)*np.array([0,1]) #740
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30)) 
        ptx =  ptx + 350 * np.array([1,0]) 
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        
        
        dwg.save()
    
    def callCWBWTop(self,fileName):
        '''
        '''
        v_width = self.dataObj.beam_L + self.dataObj.col_B/2 + 850
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-300 -300 '+str(v_width))+ ' 1400')
        
        # Cross section B-B and C-C            
        ptSecA = self.B + (20 * np.array([0,-1])) + (self.dataObj.beam_L + 350) * np.array([1,0])
        ptSecB = ptSecA + (50 * np.array([-1,0]))
        txtpt = ptSecB +(70 * np.array([-1,0])) +(20 * np.array([0,1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = self.G + (20 * np.array([0,1])) +(self.dataObj.beam_L + 350) * np.array([1,0])
        ptSecD = ptSecC + (50 * np.array([-1,0]))
        txtpt = ptSecD +(70 * np.array([-1,0])) +(20 * np.array([0,1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        
        ptSecA = self.I + (250 * np.array([0,1])) + (10* np.array([-1,0]))
        ptSecB = ptSecA + (50 * np.array([0,-1]))
        txtpt = ptSecB +(50 * np.array([0,-1])) +(15 * np.array([-1,0]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB,txtpt,txt)
        ptSecC = ptSecA + (520 * np.array([1,0]))
        ptSecD = ptSecC + (50 * np.array([0,-1]))
        txtpt = ptSecD +(50 * np.array([0,-1])) +(15 * np.array([-1,0]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD,txtpt,txt)
        
        dwg.add(dwg.line((ptSecA),(ptSecC)).stroke('#666666',width = 1.0,linecap = 'square'))
        
        dwg.add(dwg.polyline(points=[(self.A),(self.B),(self.C),(self.D),(self.E),(self.F),(self.G),(self.H),(self.I),(self.J),(self.K),(self.L),(self.A)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.dataObj.beam_L, self.dataObj.beam_B),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7),(self.A8)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.P1),(self.A6)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.P),(self.P1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.P1),(self.P2),(self.P3),(self.P7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.P7),(self.P6),(self.P5),(self.P4)], stroke='blue', fill='none', stroke_width=2.5))
        
        dwg.add(dwg.line((self.Q),(self.Q1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.Q1),(self.Q2),(self.Q3),(self.Q7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.Q7),(self.Q6),(self.Q5),(self.Q4)], stroke='blue', fill='none', stroke_width=2.5))

        

#         dwg.add(dwg.polyline([(self.ptP), (self.ptO), (self.ptR), (self.ptP)], fill='black',stroke_width=2.5,stroke='black'))
#         dwg.add(dwg.polyline([(self.ptX), (self.ptY), (self.ptZ), (self.ptX)], fill='black',stroke_width=2.5,stroke='black'))
        
        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        ptList_c = []
        ptList_c_1 = []
        if nc >= 1:
            for col in range (nc):
                pt = self.Q3  - self.dataObj.end_dist * np.array([1,0]) - (col) * self.dataObj.gauge * np.array([1,0])
                pt1 = pt - bolt_r *  np.array([1,0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2*(self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0,-1])
                B2 = pt + (rect_ht + 10) * np.array([0,1])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList.append(pt)
            if nc > 1:
                dimOffset = self.dataObj.beam_B/2 + self.dataObj.beam_tw/2 + self.dataObj.cleat_thk + 150
                pt_down = np.array(ptList[1]) + dimOffset * np.array([0,1])
                self.dataObj.drawFaintLine(np.array(ptList[1]) ,pt_down,dwg)
                params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim":10}
                self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),np.array(ptList[1]),  str(int(self.dataObj.gauge)) , params)  
        if nc_c >= 1:
            for col in range (nc_c):
                pt_c = self.Q4  + self.dataObj.cend_dist * np.array([0,1]) - self.dataObj.col_tw*np.array([1,0]) + (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c = pt_c - bolt_r *  np.array([0,1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1,0])
                B2 = pt_c + (rect_length + 10) * np.array([1,0])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                
                pt_c1 = self.P4  + self.dataObj.cend_dist * np.array([0,-1]) - self.dataObj.col_tw*np.array([1,0]) - (col) * self.dataObj.cgauge * np.array([0,1])
                pt1_c1 = pt_c1 - bolt_r *  np.array([0,1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1),fill = 'black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1,0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1,0])
                dwg.add(dwg.line((B1_1),(B2_1)).stroke('black',width = 2.5,linecap = 'square'))
                
                ptList_c.append(pt_c)
                ptList_c_1.append(pt_c1)
            if nc_c > 1:
                dimOffset = self.dataObj.beam_B/2  + self.dataObj.col_tw +100
                pt_left = np.array(ptList_c[1]) - dimOffset * np.array([1,0])
                pt_left_1 = np.array(ptList_c_1[1]) - dimOffset * np.array([1,0])
                self.dataObj.drawFaintLine(np.array(ptList_c[1]),pt_left,dwg)
                self.dataObj.drawFaintLine(np.array(ptList_c_1[1]),pt_left_1,dwg)
                params = {"offset": dimOffset, "textoffset": 50, "lineori": "right", "endlinedim":10}
                self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),np.array(ptList_c[1]),  str(int(self.dataObj.cgauge)) , params)  
                self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c_1[1]),np.array(ptList_c_1[0]),  str(int(self.dataObj.cgauge)) , params)  

            
        ###Faint lines and edge distance marking on beam connectivity
        dimOffset = self.dataObj.beam_B/2 + self.dataObj.beam_tw/2 + self.dataObj.cleat_thk + 200
        pt_down = np.array(ptList[0]) + dimOffset * np.array([0,1])
        self.dataObj.drawFaintLine(np.array(ptList[0]),pt_down,dwg)
        pt_down = self.Q3 +  dimOffset * np.array([0,1])
        self.dataObj.drawFaintLine(self.Q3,pt_down,dwg)
        params = {"offset": dimOffset , "textoffset": 20, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),self.Q3,  str(int(self.dataObj.end_dist)) , params) 
        ######Faint lines for column connectivity  edge(end) distance outer arrow
        dimOffset = self.dataObj.beam_B/2  + self.dataObj.col_tw + 100
        pt_left = np.array(ptList_c[0]) - dimOffset * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c[0]),pt_left,dwg)
        pt_left = np.array(ptList_c_1[0]) - dimOffset * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(ptList_c_1[0]),pt_left,dwg)
        pt_left = self.Q4 -  dimOffset * np.array([1,0])
        self.dataObj.drawFaintLine(self.Q4,pt_left,dwg)
        pt_left = self.P4 -  dimOffset * np.array([1,0])
        self.dataObj.drawFaintLine(self.P4,pt_left,dwg)
        params = {"offset": dimOffset, "textoffset": 50, "lineori": "right", "endlinedim":10}
        params_1 = {"offset": dimOffset, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),self.Q4 - self.dataObj.col_tw * np.array([1,0]),  str(int(self.dataObj.cend_dist)) , params_1)  
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c_1[0]),self.P4 - self.dataObj.col_tw * np.array([1,0]),  str(int(self.dataObj.cend_dist)) , params) 
        c_gauge  = 2 * self.dataObj.cleat_legsize_1 + self.dataObj.beam_tw - 2 * self.dataObj.cend_dist
        
        params = {"offset": dimOffset, "textoffset": 75, "lineori": "right", "endlinedim":10}
        if self.dataObj.no_of_ccol > 1:
            self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[1]),np.array(ptList_c_1[1]) , str(int(c_gauge)) , params)
        else:
            self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList_c[0]),np.array(ptList_c_1[0]) , str(int(c_gauge)) , params)
        
        # Beam Information
        beam_pt = self.A6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
        
        # column  Information
        col_pt = (self.A + self.B)/4
        theta = 90
        offset = 100
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NW", offset, textUp, textDown)
        
        #Cleat Information
        plt_pt = self.P3 
        theta = 45
        offset =  self.dataObj.beam_B /2 + 50
        textUp = "ISA." + str(int(self.dataObj.cleat_legsize))+'x'+ str(int(self.dataObj.cleat_legsize_1))+ 'x' + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown)
        
        
        # beam Bolt Information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col 
        
        bltPt = np.array(ptList[0]) 
        theta = 45
        offset = (self.dataObj.D_col - self.dataObj.beam_B)/2 + 100
        textUp = str(no_of_bbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp,textDown)
        
        # column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        
        weldPt = np.array(ptList_c[0])
        theta = 45
        offset = self.dataObj.D_col* 3/4 + 50
        textUp = str(no_of_cbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown)
        
        # Gap Informatoin
        ptG1 = self.D + 100 * np.array([0,-1])
        ptG2 = ptG1 + self.dataObj.gap * np.array([1,0]) 
        offset = 100
        params = {"offset": offset, "textoffset": 10, "lineori": "left", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)
        # Draw Faint Lines to representation of Gap distance #
        ptA = self.D
        ptB = ptA + (200) * np.array([0,-1]) 
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.A1
        ptD = ptC + (200) * np.array([0,-1]) - (self.dataObj.D_col - 2 * self.dataObj.col_T - self.dataObj.beam_B) / 2 * np.array([0,1])
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
        
        
        
        # 2D view name
        ptx =  self.A + (80)* np.array([1,0]) +800* np.array([0,1]) #1090
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 32)) 
        ptx =  ptx + 350 * np.array([1,0]) 
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        dwg.save()



            
class cleat2DCreatorSide(object):
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        
        # CWBW connectivity points
        self.A = np.array([0,0])
        self.B = self.A + self.dataObj.col_T * np.array([1,0])
        self.C = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1,0])
        self.D = self.A + self.dataObj.D_col * np.array([1,0])
        self.H = self.C + self.dataObj.col_L * np.array([0,1])
        self.G = self.B + self.dataObj.col_L * np.array([0,1])
        self.A1 = ((self.dataObj.D_col - self.dataObj.beam_B)/2) * np.array([1,0]) + ((self.dataObj.col_L - self.dataObj.D_beam)/2) * np.array([0,1])
        self.A2 = self.A1 + self.dataObj.beam_B * np.array([1,0])
        self.A3 = self.A2 + self.dataObj.beam_T * np.array([0,1])
        self.A12 = self.A1 + self.dataObj.beam_T * np.array([0,1])
        self.A11 = self.A12 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([1,0])
        self.A4 = self.A11 + self.dataObj.beam_tw * np.array([1,0])
        self.A5 = self.A4 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.A6 = self.A2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.A7 = self.A2 + self.dataObj.D_beam * np.array([0,1])
        self.A8 = self.A1 + self.dataObj.D_beam * np.array([0,1])
        self.A9 = self.A1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.A10 = self.A11 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.P = self.A11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
        self.Q = self.P + self.dataObj.cleat_thk * np.array([-1,0])
        self.X = self.P + self.dataObj.cleat_legsize_1 * np.array([-1,0])
        self.R = self.P + self.dataObj.cleat_ht * np.array([0,1])
        
        
        self.P1 = self.P + (self.dataObj.beam_tw) * np.array([1,0])
        self.Q1 = self.P1 + self.dataObj.cleat_thk * np.array([1,0])
        self.X1 = self.P1+ self.dataObj.cleat_legsize_1 * np.array([1,0])
        self.R1 = self.P1 + self.dataObj.cleat_ht * np.array([0,1])
        
        #### CFBW connectivity
        self.FA = np.array([0,0])
        self.FB = self.FA + self.dataObj.col_B * np.array([1,0])
        self.ptMid = self.FA + ((self.dataObj.col_B/2) + (self.dataObj.col_tw/2))* np.array([1,0])
        self.ptMid1 = self.ptMid + ((self.dataObj.col_L - self.dataObj.D_beam)/2) * np.array([0,1])
        self.FC = self.FB + self.dataObj.col_L * np.array([0,1])
        self.FD = self.FA + self.dataObj.col_L * np.array([0,1])
        self.FA1 = self.FA + (self.dataObj.col_B - self.dataObj.beam_B)/2 * np.array([1,0]) + (self.dataObj.col_L - self.dataObj.D_beam)/2 * np.array([0,1])
        self.FA2 = self.FA1 + self.dataObj.beam_B * np.array([1,0])
        self.FA3 = self.FA2 + self.dataObj.beam_T * np.array([0,1])
        self.FA12 = self.FA1 + self.dataObj.beam_T * np.array([0,1])
        self.FA11 = self.FA12 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([1,0])
        self.FA4 = self.FA11 + self.dataObj.beam_tw * np.array([1,0])
        self.FA5 = self.FA4 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.FA6 = self.FA2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.FA7 = self.FA2 + self.dataObj.D_beam * np.array([0,1])
        self.FA8 = self.FA1 + self.dataObj.D_beam * np.array([0,1])
        self.FA9 = self.FA1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.FA10 = self.FA11 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
#         self.FP = self.FA11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
#         self.FQ = self.FP + self.dataObj.cleat_thk * np.array([-1,0])
#         self.FX = self.FQ + self.dataObj.cleat_thk * np.array([-1,0])
#         self.FR = self.FP + self.dataObj.cleat_ht * np.array([0,1])
#         self.FY = self.FX + self.dataObj.cleat_ht * np.array([0,1])
        
        self.FP = self.FA11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
        self.FQ = self.FP + self.dataObj.cleat_thk * np.array([-1,0])
        self.FX = self.FP + self.dataObj.cleat_legsize_1 * np.array([-1,0])
        self.FP2 = self.FP + self.dataObj.cleat_ht * np.array([0,1])
        self.FQ2 = self.FQ + self.dataObj.cleat_ht * np.array([0,1])
        self.FX2 = self.FX + self.dataObj.cleat_ht * np.array([0,1])
        
        
        self.FP1 = self.FP + (self.dataObj.beam_tw) * np.array([1,0])
        self.FQ1 = self.FP1 + self.dataObj.cleat_thk * np.array([1,0])
        self.FX1 = self.FP1+ self.dataObj.cleat_legsize_1 * np.array([1,0])
        self.FP3 = self.FP1 + self.dataObj.cleat_ht * np.array([0,1])
        self.FQ3 = self.FQ1 + self.dataObj.cleat_ht * np.array([0,1])
        self.FX3 = self.FX1 + self.dataObj.cleat_ht * np.array([0,1])
        
        ##### Points for Beam-Beam connection #####
        
        self.beam_beam_length = self.dataObj.beam_B + 200 ##beam_B
        
        # for primary beam
        
        self.BA = (0,0)
        self.BB = self.BA + (self.beam_beam_length) *np.array([1,0]) # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS
        self.BC = self.BB + (self.dataObj.col_T) * np.array([0,1])
        self.BD = self.BC - (self.beam_beam_length - self.dataObj.beam_tw)/2 * np.array([1,0]) # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS
        self.BE = self.BD - self.dataObj.beam_tw * np.array([1,0]) # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS :BEAM_TW
        self.BF = self.BA + self.dataObj.col_T * np.array([0,1])
        self.BG = self.BA + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0,1])
        self.BH = self.BG + self.beam_beam_length * np.array([1,0])
        self.BI = self.BH + self.dataObj.col_T * np.array([0,1])
        self.BJ = self.BG + self.dataObj.col_T * np.array([0,1])
        
        
        # for secondary beam ### changes after importing beam
        
        self.BA1 = self.BA + (self.beam_beam_length - self.dataObj.beam_B)/2 * np.array([1,0]) # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS :BEAM_B
        self.BB1 = self.BA1 + (self.dataObj.beam_B) * np.array([1,0]) # BEAM_B
        self.BC1 = self.BB1 + (self.dataObj.beam_T) * np.array([0,1])
        self.BD1 = self.BC1 - (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([1,0])
        self.BE1 = self.BD1 + (self.dataObj.D_beam - 2*self.dataObj.beam_T) * np.array([0,1])
        self.BF1 = self.BC1 + (self.dataObj.D_beam - 2*self.dataObj.beam_T) * np.array([0,1])
        self.BG1 = self.BF1 + (self.dataObj.beam_T) * np.array([0,1])
        self.BL1 = self.BA1 + (self.dataObj.beam_T) * np.array([0,1])
        self.BH1 = self.BL1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1]) 
        self.BI1 = self.BL1 + (self.dataObj.D_beam - 2*self.dataObj.beam_T) * np.array([0,1])
        self.BJ1 = self.BE1 - self.dataObj.beam_tw * np.array([1,0])
        self.BK1 = self.BD1 - self.dataObj.beam_tw * np.array([1,0])
        
        # for cleat angle
        
        self.BP = self.BD + (self.dataObj.notch_offset - self.dataObj.col_T) * np.array([0,1])
        self.BQ = self.BP + self.dataObj.cleat_thk * np.array([1,0])
        self.BR = self.BP + self.dataObj.cleat_legsize_1 * np.array([1,0])
        self.BP1 = self.BP + self.dataObj.cleat_ht * np.array([0,1])
        self.BQ1 = self.BQ + self.dataObj.cleat_ht * np.array([0,1])
        self.BR1 = self.BR + self.dataObj.cleat_ht * np.array([0,1])
        self.BX = self.BP - self.dataObj.beam_tw * np.array([1,0])#beam_tw
        self.BY = self.BX - self.dataObj.cleat_thk * np.array([1,0])
        self.BZ = self.BX - self.dataObj.cleat_legsize_1 * np.array([1,0])
        self.BX1 = self.BX + self.dataObj.cleat_ht * np.array([0,1])
        self.BY1 = self.BY + self.dataObj.cleat_ht * np.array([0,1])
        self.BZ1 = self.BZ + self.dataObj.cleat_ht * np.array([0,1])
        
    def callBWBWSide(self,fileName):
        dwg = svgwrite.Drawing(fileName,size=('100%', '100%'), viewBox=('-500 -400 1500 1400'))
        dwg.add(dwg.polyline(points=[(self.BA),(self.BB),(self.BI),(self.BJ),(self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BG),(self.BH)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.BF),(self.BE)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.BD),(self.BC)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.BE),(self.BD)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline(points=[(self.BB1),(self.BC1),(self.BD1),(self.BE1),(self.BF1),(self.BG1),(self.BH1),(self.BI1),(self.BJ1),(self.BK1),(self.BL1),(self.BA1)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BQ), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
#         dwg.add(dwg.rect(insert=(self.BX), size=(-self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
#         dwg.add(dwg.rect(insert=(self.BY), size=(-(self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BY), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BZ), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))

        
        ####################Arrangng Bolts on both beams #######################
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitchPts = []
        pitchPts_c = []
        pitchPts_c_1 = []
        for row in range(nr):
                
            pt = self.BY + self.dataObj.edge_dist * np.array([0,1])+ (row) *self.dataObj.pitch  * np.array([0,1])
            pt1 = pt - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length,rect_width),fill = "black", stroke='none', stroke_width=2.5))
            blt1 = pt -5*np.array([1,0])
            blt2 = pt + (5+ rect_length) *np.array([1,0])
            dwg.add(dwg.line((blt1),(blt2)).stroke('black',width = 1.5,linecap = 'square'))
            pitchPts.append(pt)
            
        for row1 in range(c_nr):
            colList = [] #CHANGE NAME
            colList_c = [] #CHANGE NAME
            for col in range(c_nc): #CHANGE cpitch,cend_dist,cedge_dist to bpitch etc in future after supported beam array imported
                pt_c = self.BZ + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt_c), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1),(cbolt2)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3),(cbolt4)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                pt_c1 = self.BR + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([-1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt_c1), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1_1),(cbolt2_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3_1),(cbolt4_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                colList.append(pt_c)
                colList_c.append(pt_c1)
            pitchPts_c.append(colList)
            pitchPts_c_1.append(colList_c)
        

        
 ##################### Faint Lines and outer arrow for suporting beam connectivity ############  
        length = (self.beam_beam_length - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw)/2 #beam_tw
        pt_right = self.BR + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(self.BR,pt_right,dwg)
        pt  = self.BR1
        pt_right = self.BR1 + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_right,dwg)
        
        pt_right = np.array(pitchPts_c_1[0][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[0][0]),pt_right,dwg)
        pt_right = np.array(pitchPts_c_1[-1][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_right,dwg)
         
        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,self.BR, self.BR1, str(int(self.dataObj.cleat_ht)), params) 
        
        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts_c_1[0][0]), np.array(pitchPts_c_1[-1][0]),  str(len(pitchPts_c_1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)
         
        pt_up = np.array(pitchPts_c_1[0][0]) - self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params) 
         
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params)
        ####notch height###############
        self.dataObj.drawFaintLine(self.BB,self.BB + 200 * np.array([1,0]),dwg)
        pt_down = self.BB + self.dataObj.notch_offset * np.array([0,1])
        params = {"offset": 200, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,self.BB, pt_down, str(int(self.dataObj.notch_offset)), params)        
         
        
        ############Vertical column marking ###############
        v_length = (self.dataObj.D_col - self.dataObj.cleat_ht - self.dataObj.notch_offset) +50   
        ptY = self.BZ1
        ptY1 = self.BR1
        ptY_down = ptY + v_length * np.array([0,1])
        ptY1_down = ptY1 + v_length * np.array([0,1])
        self.dataObj.drawFaintLine(ptY,ptY_down,dwg)
        self.dataObj.drawFaintLine(ptY1,ptY1_down,dwg)
        
        pt_bolt = np.array(pitchPts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        pt_bolt_1 = np.array(pitchPts_c_1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_bolt_1,dwg)
        self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][0]),pt_bolt,dwg)
        
        pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 50, "lineori": "right", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY, pt_down, str(int(self.dataObj.cend_dist)), params)
        
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 50, "lineori": "left", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)  
        
        if c_nc > 1:
            pt_bolt_down = np.array(pitchPts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            pt_bolt_1_down = np.array(pitchPts_c_1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][-1]),pt_bolt_1_down,dwg)
            self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][-1]),pt_bolt_down,dwg)
            
            pt_down = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 50, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 50, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw  #Beam_tw
            params = {"offset": v_length + 100, "textoffset": 50, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)  
            
        else:
            pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * ( self.dataObj.cend_dist) - self.dataObj.beam_tw #Beam_tw
            params = {"offset": v_length + 100, "textoffset": 50, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)
               
    
    ####################### Faint Lines and outer arrow for beam connectivity ############
        
        length = self.beam_beam_length/2 -self.dataObj.beam_tw/2 - self.dataObj.cleat_thk  #Beam_tw
        ptQ1 = self.BY
        pt_left = ptQ1 -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(ptQ1,pt_left,dwg)
        pt  = ptQ1 + self.dataObj.cleat_ht * np.array([0,1])
        pt_left = pt -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_left,dwg)
        
        pt_left = np.array(pitchPts[0]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[0]),pt_left,dwg)
        pt_left = np.array(pitchPts[-1]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[-1]),pt_left,dwg)
        
        offset =length + 100
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[-1]),  str(len(pitchPts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
         
        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[0]), ptQ1, str(int(self.dataObj.edge_dist)) , params) 
         
        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[-1]), pt, str(int(self.dataObj.edge_dist)), params)
    ###################################################################################################################            
        # SUPORTED BEAM Designation
        beam_pt = self.BG1
        theta = 30
        offset = (self.beam_beam_length - self.dataObj.beam_B)/2 + 25#beam_B
        textUp = "Beam " + self.dataObj.beam_Designation ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
    
        # SUPORTING BEAM Designation
        theta = 90
        offset = 0.0
        textUp =  "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, self.BA, theta, "NW", offset, textUp,textDown)
            
        #  primary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol
                
        bltPtx = np.array(pitchPts_c_1[0][0])
        theta = 45
        offset = (self.dataObj.D_beam *3)/8 + 75 ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)
       
        # secondary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col#Double Angle cleat
          
        bltPt = np.array(pitchPts[0])
        theta = 70
        offset = (self.beam_beam_length/2 + 50) ##
        textUp = str(no_of_bolts) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')' ##NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NW", offset, textUp,textDown)        
        
        
        
        # cleat angle information
        cleatPt = self.BZ1 
        theta = 30
        offset = (self.beam_beam_length - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw/(3.46))#beam_tw
        textUp = "ISA." + str(int(self.dataObj.cleat_legsize)) +"X" + str(int(self.dataObj.cleat_legsize_1)) +"X" + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, cleatPt, theta, "SW", offset, textUp, textDown)
        
        # 2D view name
        ptx =  self.BA + 10 * np.array([1,0]) + 800 * np.array([0,1]) #980
        dwg.add(dwg.text('Side View (Sec B-B)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        ## All dimensions in "mm"
        ptx =  ptx +  350 * np.array([1,0])
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30))
        dwg.save()
        
    
    def callCWBWSide(self,fileName):
        '''
        '''
        v_width = self.dataObj.D_col + 500 + 500 
        dwg = svgwrite.Drawing(fileName,size=('100%', '100%'), viewBox=('-500 -300 ' + str(v_width) + ' 1600'))
        dwg.add(dwg.rect(insert=(self.A), size=(self.dataObj.D_col, self.dataObj.col_L),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.C),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.B),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.A1),(self.A2),(self.A3),(self.A4),(self.A5),(self.A6),(self.A7),(self.A8),(self.A9),(self.A10),(self.A11),(self.A12),(self.A1)], stroke='blue', fill='none', stroke_width=2.5))
        

        dwg.add(dwg.rect(insert=(self.X), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = "none", stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.Q), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.Q1), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = "none", stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.P1), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitchPts = []
        pitchPts_c = []
        pitchPts_c_1 = []
        for row in range(nr):
                
            pt = self.Q + self.dataObj.edge_dist * np.array([0,1])+ (row) *self.dataObj.pitch  * np.array([0,1])
            pt1 = pt - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length,rect_width),fill = "black", stroke='none', stroke_width=2.5))
            blt1 = pt -5*np.array([1,0])
            blt2 = pt + (5+ rect_length) *np.array([1,0])
            dwg.add(dwg.line((blt1),(blt2)).stroke('black',width = 1.5,linecap = 'square'))
            pitchPts.append(pt)
            
        for row1 in range(c_nr):
            colList = []
            colList_c = []
            for col in range(c_nc):
                pt_c = self.X + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt_c), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1),(cbolt2)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3),(cbolt4)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                pt_c1 = self.X1 + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([-1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt_c1), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1_1),(cbolt2_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3_1),(cbolt4_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                colList.append(pt_c)
                colList_c.append(pt_c1)
            pitchPts_c.append(colList)
            pitchPts_c_1.append(colList_c)
        
             
    ##################### Faint Lines and outer arrow for suporting beam connectivity ############  
        length = (self.dataObj.D_col - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw)/2
        pt_right = self.X1 + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(self.X1,pt_right,dwg)
        pt  = self.X1 + self.dataObj.cleat_ht * np.array([0,1])
        pt_right = self.X1 + self.dataObj.cleat_ht * np.array([0,1]) + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_right,dwg)
        
        pt_right = np.array(pitchPts_c_1[0][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[0][0]),pt_right,dwg)
        pt_right = np.array(pitchPts_c_1[-1][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_right,dwg)
         
        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,self.X1, self.X1 + self.dataObj.cleat_ht * np.array([0,1]), str(int(self.dataObj.cleat_ht)), params) 
        
        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts_c_1[0][0]), np.array(pitchPts_c_1[-1][0]),  str(len(pitchPts_c_1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)
         
        pt_up = np.array(pitchPts_c_1[0][0]) - self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params) 
         
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params) 
        
        ############Vertical column marking ###############
        v_length = self.dataObj.col_L/2 + self.dataObj.cleat_ht/2
        ptY = self.X + self.dataObj.cleat_ht * np.array([0,1])
        ptY1 = self.X1 + self.dataObj.cleat_ht * np.array([0,1])
        ptY_down = ptY + v_length * np.array([0,1])
        ptY1_down = ptY1 + v_length * np.array([0,1])
        self.dataObj.drawFaintLine(ptY,ptY_down,dwg)
        self.dataObj.drawFaintLine(ptY1,ptY1_down,dwg)
        
        pt_bolt = np.array(pitchPts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        pt_bolt_1 = np.array(pitchPts_c_1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_bolt_1,dwg)
        self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][0]),pt_bolt,dwg)
        
        pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "right", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY, pt_down, str(int(self.dataObj.cend_dist)), params)
        
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "left", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)  
        
        if c_nc > 1:
            pt_bolt_down = np.array(pitchPts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            pt_bolt_1_down = np.array(pitchPts_c_1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][-1]),pt_bolt_1_down,dwg)
            self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][-1]),pt_bolt_down,dwg)
            
            pt_down = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 100, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)  
            
        else:
            pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * ( self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)
               
    
    ####################### Faint Lines and outer arrow for beam connectivity ############
        
        length = self.dataObj.D_col/2 -self.dataObj.beam_tw/2 - self.dataObj.cleat_thk 
        ptQ1 = self.P - self.dataObj.cleat_thk * np.array([1,0])
        pt_left = ptQ1 -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(ptQ1,pt_left,dwg)
        pt  = ptQ1 + self.dataObj.cleat_ht * np.array([0,1])
        pt_left = pt -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_left,dwg)
        
        pt_left = np.array(pitchPts[0]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[0]),pt_left,dwg)
        pt_left = np.array(pitchPts[-1]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[-1]),pt_left,dwg)
        
        offset =length + 100
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[-1]),  str(len(pitchPts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
         
        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[0]), ptQ1, str(int(self.dataObj.edge_dist)) , params) 
         
        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[-1]), pt, str(int(self.dataObj.edge_dist)), params)
    
    ###################################################################################################################    
    ###### Beam Information
        beam_pt = self.A2
        theta = 45
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
               
#       column  Information
        col_pt = self.A
        theta = 45
        offset = 50
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NW", offset, textUp, textDown)
         
#       cleat Angle Information
        beam_pt = self.R + self.dataObj.cleat_thk/2 * np.array([-1,0])
        theta = 45
        offset =  self.dataObj.cleat_thk + self.dataObj.beam_B /2 + 80
        textUp = "ISA. " + str(int(self.dataObj.cleat_legsize))+'x'+ str(int(self.dataObj.cleat_legsize_1))+ 'x' + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
         
#       beam bolt information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        boltPt = np.array(pitchPts[0])
        theta = 45
        offset = (self.dataObj.D_col)/2 + 10
        textUp = str(no_of_bbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, boltPt, theta, "NW", offset, textUp, textDown)
#       column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol
        
        boltPt = np.array(pitchPts_c_1[0][0])
        theta = 45
        offset = (self.dataObj.D_col - self.dataObj.beam_B)/2  + self.dataObj.cend_dist + 10
        textUp = str(no_of_cbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, boltPt, theta, "NE", offset, textUp, textDown)
    
        
        # 2D view name
        ptx =  self.A + (1290)* np.array([0,1]) + 75 * np.array([1,0])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30)) 
        ## All dimensions in "mm"
        ptx2 =  ptx + 350 * np.array([1,0])
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx2), fill='black',font_family = "sans-serif",font_size = 30))      
        dwg.save()
    
    def callCFBWSide(self,fileName):
        '''
        '''
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-350 -300 1200 1500'))
        dwg.add(dwg.rect(insert=(self.FA), size=(self.dataObj.col_B, self.dataObj.col_L),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[(self.FA1),(self.FA2),(self.FA3),(self.FA4),(self.FA5),(self.FA6),(self.FA7),(self.FA8),(self.FA9),(self.FA10),(self.FA11),(self.FA12),(self.FA1)], stroke='blue', fill='none', stroke_width=2.5))
      
        dwg.add(dwg.rect(insert=(self.FX), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = "none", stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FQ), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FQ1), size=((self.dataObj.cleat_legsize_1-self.dataObj.cleat_thk), self.dataObj.cleat_ht),fill = "none", stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP1), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        nr = self.dataObj.no_of_rows
        bolt_r = self.dataObj.bolt_dia/2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitchPts = []
        pitchPts_c = []
        pitchPts_c_1 = []
        for row in range(nr):
                
            pt = self.FQ + self.dataObj.edge_dist * np.array([0,1])+ (row) *self.dataObj.pitch  * np.array([0,1])
            pt1 = pt - bolt_r * np.array([0,1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length,rect_width),fill = "black", stroke='none', stroke_width=2.5))
            blt1 = pt -5*np.array([1,0])
            blt2 = pt + (5+ rect_length) *np.array([1,0])
            dwg.add(dwg.line((blt1),(blt2)).stroke('black',width = 1.5,linecap = 'square'))
            pitchPts.append(pt)
            
        for row1 in range(c_nr):
            colList = []
            colList_1 = []
            for col in range(c_nc):
                pt_c = self.FX + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt_c), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1),(cbolt2)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3),(cbolt4)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                pt_c1 = self.FX1 + self.dataObj.cedge_dist * np.array([0,1]) + (self.dataObj.cend_dist)* np.array([-1,0]) + (row1) *self.dataObj.cpitch  * np.array([0,1]) + (col) * self.dataObj.cgauge * np.array([-1,0])
                dwg.add(dwg.circle(center=(pt_c1), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([1,0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([-1,0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia/2 + 4) *np.array([0,-1])
                dwg.add(dwg.line((cbolt1_1),(cbolt2_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                dwg.add(dwg.line((cbolt3_1),(cbolt4_1)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10,5,1,5])))
                
                colList.append(pt_c)
                colList_1.append(pt_c1)
            pitchPts_c.append(colList)
            pitchPts_c_1.append(colList_1)
                            

        
         
    ##################### Faint Lines and outer arrow for Primary beam connectivity ############  
        length = (self.dataObj.col_B - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw)/2 + 50
        pt_right = self.FX1 + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(self.FX1,pt_right,dwg)
        pt  = self.FX1 + self.dataObj.cleat_ht * np.array([0,1])
        pt_right = self.FX1 + self.dataObj.cleat_ht * np.array([0,1]) + (length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_right,dwg)
        
        pt_right = np.array(pitchPts_c_1[0][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[0][0]),pt_right,dwg)
        pt_right = np.array(pitchPts_c_1[-1][0])+ (self.dataObj.cend_dist + length +200) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_right,dwg)
         
        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,self.X1, self.X1 + self.dataObj.cleat_ht * np.array([0,1]), str(int(self.dataObj.cleat_ht)), params) 
        
        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts_c_1[0][0]), np.array(pitchPts_c_1[-1][0]),  str(len(pitchPts_c_1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)
         
        pt_up = np.array(pitchPts_c_1[0][0]) - self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params) 
         
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts_c_1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params) 
        
        ############Vertical column marking ###############
        v_length = (self.dataObj.col_L- self.dataObj.D_beam)/2 + self.dataObj.D_beam/2 - (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptY = self.FX + self.dataObj.cleat_ht * np.array([0,1])
        ptY1 = self.FX1 + self.dataObj.cleat_ht * np.array([0,1])
        ptY_down = ptY + v_length * np.array([0,1])
        ptY1_down = ptY1 + v_length * np.array([0,1])
        self.dataObj.drawFaintLine(ptY,ptY_down,dwg)
        self.dataObj.drawFaintLine(ptY1,ptY1_down,dwg)
        
        pt_bolt = np.array(pitchPts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        pt_bolt_1 = np.array(pitchPts_c_1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0,1])
        self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][0]),pt_bolt_1,dwg)
        self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][0]),pt_bolt,dwg)
        
        pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "right", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY, pt_down, str(int(self.dataObj.cend_dist)), params)
        
        pt_down = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "left", "endlinedim":20}
        self.dataObj.draw_dimension_outerArrow(dwg,ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)  
        
        if c_nc > 1:
            pt_bolt_down = np.array(pitchPts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            pt_bolt_1_down = np.array(pitchPts_c_1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0,1])
            self.dataObj.drawFaintLine(np.array(pitchPts_c_1[-1][-1]),pt_bolt_1_down,dwg)
            self.dataObj.drawFaintLine(np.array(pitchPts_c[-1][-1]),pt_bolt_down,dwg)
            
            pt_down = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(self.dataObj.cgauge)) , params)  
            
            pt_down = np.array(pitchPts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][-1]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 100, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)  
            
        else:
            pt_down = np.array(pitchPts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            pt_down_left = np.array(pitchPts_c_1[-1][0]) + self.dataObj.cedge_dist * np.array([0,1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * ( self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg,pt_down, pt_down_left, str(int(c_gauge)) , params)
               
    
    ####################### Faint Lines and outer arrow for beam connectivity ############
        
        length = self.dataObj.col_B/2 -self.dataObj.beam_tw/2 - self.dataObj.cleat_thk 
        ptQ1 = self.FP - self.dataObj.cleat_thk * np.array([1,0])
        pt_left = ptQ1 -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(ptQ1,pt_left,dwg)
        pt  = ptQ1 + self.dataObj.cleat_ht * np.array([0,1])
        pt_left = pt -   (length +100) * np.array([1,0])
        self.dataObj.drawFaintLine(pt,pt_left,dwg)
        
        pt_left = np.array(pitchPts[0]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[0]),pt_left,dwg)
        pt_left = np.array(pitchPts[-1]) - (length + 100) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[-1]),pt_left,dwg)
        
        offset =length + 100
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[-1]),  str(len(pitchPts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
         
        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[0]), ptQ1, str(int(self.dataObj.edge_dist)) , params) 
         
        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,np.array(pitchPts[-1]), pt, str(int(self.dataObj.edge_dist)), params)
    
    ###################################################################################################################    
    ##### Beam Information
        beam_pt = (self.FA2 + self.FA1)/2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + 25
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
                
       #column  Information
        col_pt = self.FA
        theta = 45
        offset = 50
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NW", offset, textUp, textDown)
          
    #cleat Angle Information
        beam_pt = (self.FX3)
        theta = 30
        offset =  self.dataObj.cleat_ht/2
        textUp = "ISA. " + str(int(self.dataObj.cleat_legsize))+'x'+ str(int(self.dataObj.cleat_legsize_1))+ 'x' + str(int(self.dataObj.cleat_thk))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
          
    #beam bolt information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        boltPt = np.array(pitchPts[0])
        theta = 45
        offset = (self.dataObj.col_B)/2 + 70
        textUp = str(no_of_bbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, boltPt, theta, "NW", offset, textUp, textDown)
    #column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * 2 *self.dataObj.no_of_ccol
        boltPt = np.array(pitchPts_c_1[0][0])
        theta = 45
        offset = (self.dataObj.D_col - self.dataObj.beam_B)/2  + self.dataObj.cend_dist + 50
        textUp = str(no_of_cbolts ) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.drawOrientedArrow(dwg, boltPt, theta, "NE", offset, textUp, textDown)
    
        
        # 2D view name
        ptx =  self.A + (1010)* np.array([0,1]) + 50 * np.array([1,0]) #1190
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black',font_family = "sans-serif",font_size = 30)) 
        ## All dimensions in "mm"
        ptx2 =  ptx + 350 * np.array([1,0])
        dwg.add(dwg.text('(All distances are in "mm")', insert=(ptx2), fill='black',font_family = "sans-serif",font_size = 30))      
        dwg.save()
        



 
 
 
     
     
     