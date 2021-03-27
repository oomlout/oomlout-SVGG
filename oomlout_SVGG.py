import time
import subprocess

import svgwrite
from svgwrite.extensions import Inkscape
from svgwrite import cm, mm 



######  SVGWRITE Routines    


def ooI(dwg, name, coord, size=(0, 0), rx=5*mm, stroke_width=0.25*mm, sty="", stroke='black', fill='none', rotate=0, text=""):
        oomInsert(dwg, name, coord, size, rx, stroke_width, sty, stroke, fill, rotate, text) 

def oomInsert(dwg, name, coord, size=(0, 0), rx=5*mm, stroke_width=0.25*mm, sty="", stroke='black', fill='none', rotate=0, text=""):
        print("    Adding: " + name + " (" + str(coord[0]) +"," + str(coord[1]) + ")" + " (" + str(size[0]) +  "," + str(size[1]) + ")")
        if name == "rectangle" or name == "rect" or name == "r" :
            dwg.add(oomRect(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty=sty, stroke='black', fill='none'))            
        elif name == "rectRounded" or  name == "rr" or  name == "rectangleRounded":
            dwg.add(oomRect(dwg, coord, size, rx=10, stroke_width=0.25*mm, sty=sty, stroke='black', fill='none'))
        elif name == "circle":
            dwg.add(oomCircle(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        elif name == "oobb" or name == "o" or  name == "ob":
            oomInsertOOBB(dwg, coord,stroke_width=0.25*mm, sty=sty, stroke='black', fill='none')
        elif name == "oobbt" or  name == "ot": #bolt hole
            oomInsertOOBBT(dwg, coord,stroke_width=0.25*mm, sty=sty, stroke='black', fill='none', rotate=rotate)
        elif name == "oobbSlot" or  name == "os": #slot
            oomInsertOOBBSlot(dwg, coord,stroke_width=0.25*mm, sty=sty, stroke='black', fill='none', rotate=rotate)
        elif name == "text" or  name == "t": #text
            dwg.add(oomText(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty=sty, stroke='black', fill='none', text=text))            

def oomRectRounded(dwg, coord, size, rx=5*mm, stroke_width=0.25*mm, sty='', stroke='black', fill='none'): ##takes in mm
    return oomRect(dwg, coord, size, rx=rx, stroke_width=0.25*mm, sty="", stroke='black', fill='none')

def oomRect(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'): ##takes in mm
    laserLineWidth = 0.25*mm
    if sty != "":
        stroke_width=laserLineWidth
        fill='none'
        if sty == "cut":
            stroke='black'        
        elif sty == "etch":
            stroke='purple'        
        elif sty == "trace":
            stroke='blue'        
        elif sty == "dash":
            stroke='green'        
        elif sty == "comment":
            stroke='cyan'
            fill='cyan'
    x = coord[0]
    y = coord[1]
    width = size[0]
    height = size[1]

    x = x - width/2
    y = y - height/2

    return dwg.rect((x*mm, y*mm), (width*mm, height*mm), rx=rx, ry=rx, stroke_width=stroke_width, fill=fill, stroke=stroke)

def oomText(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none',text=""): ##takes in mm
    print("    Text: " + text)
    laserLineWidth = 0.25*mm
    if sty != "":
        stroke_width=laserLineWidth
        fill='none'
        if sty == "cut":
            stroke='black'        
        elif sty == "etch":
            stroke='purple'        
        elif sty == "trace":
            stroke='blue'        
        elif sty == "dash":
            stroke='green'        
        elif sty == "comment":
            stroke='cyan'        
    x = coord[0]
    y = coord[1]
    width = size[0]
    height = size[1]

    x = x - width/2
    y = y - height/2

    return dwg.text(text,(x*mm, y*mm), font_size=36, stroke_width=stroke_width, fill=fill, stroke=stroke)

def oomCircle(dwg, coord, size, rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'): ##takes in mm
    laserLineWidth = 0.25*mm
    if sty != "":
        stroke_width=laserLineWidth
        fill='none'
        if sty == "cut":
            stroke='black'        
        elif sty == "etch":
            stroke='purple'        
        elif sty == "trace":
            stroke='blue'        
        elif sty == "dash":
            stroke='green'        
        elif sty == "comment":
            stroke='cyan'        
    x = coord[0]
    y = coord[1]
    width = size[0]
    height = size[1]

    x = x
    y = y

    return dwg.ellipse((x*mm, y*mm), (width/2*mm, height/2*mm), stroke_width=stroke_width, fill=fill, stroke=stroke)

def oomInsertOOBB(dwg, coord, stroke_width=0.25*mm, sty="", stroke='black', fill='none'): 
    dwg.add(oomRect(dwg, coord, (3, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    dwg.add(oomRect(dwg, coord, (6, 3), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    dwg.add(oomCircle(dwg, coord, (6, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
                               
def oomInsertOOBBT(dwg, coord, stroke_width=0.25*mm, sty="", stroke='black', fill='none',rotate=0): 
    m16 = True

    if rotate == 0:
        dwg.add(oomRect(dwg, (coord[0],coord[1]+5/2), (6, 5), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0],coord[1]+5+6/2), (10, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    elif rotate == 90:
        dwg.add(oomRect(dwg, (coord[0]+5/2,coord[1]), (5, 6), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0]+5+6/2,coord[1]), (6, 10), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0]-3/2,coord[1]+15), (3, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0]-3/2,coord[1]-15), (3, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        if m16:
            dwg.add(oomRect(dwg, (coord[0]+5+6+5/2,coord[1]), (5, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    elif rotate == 180:
        dwg.add(oomRect(dwg, (coord[0],coord[1]-5/2), (6, 5), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0],coord[1]-5-6/2), (10, 6), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    elif rotate == 270:
        dwg.add(oomRect(dwg, (coord[0]-5/2,coord[1]), (5, 6), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        dwg.add(oomRect(dwg, (coord[0]-5-6/2,coord[1]), (6, 10), rx=0, stroke_width=0.25*mm, sty="", stroke='black', fill='none'))

def oomInsertOOBBSlot(dwg, coord, stroke_width=0.25*mm, sty="", stroke='black', fill='none',rotate=0): 
    if rotate == 0:
        dwg.add(oomRect(dwg, (coord[0],coord[1]), (6, 3), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
    elif rotate == 90:
        dwg.add(oomRect(dwg, (coord[0],coord[1]), (3, 6), stroke_width=0.25*mm, sty="", stroke='black', fill='none'))
        
       
                                                         
def searchAndReplaceSVG(loi,inFile,outFile):
    f = open(inFile)
    contents = f.read()
    f.close()

    for x in loi:
        #print("            Replacing: " + str(x[0]) + "   "  + str(x[1]))
        skips = ["name"]
        if x[0] in skips:       ##Need to do a strict replace for common ones
            contents = contents.replace(">" + str(x[0]) + "<",">" + str(x[1]) + "<")
        else:            
            contents = contents.replace(str(x[0]),str(x[1]))
        
    f = open(outFile,"w+")
    f.write(contents)
    f.close

def searchAndReplaceSVGStrict(loi,inFile,outFile):
    f = open(inFile)
    contents = f.read()
    f.close()

    for x in loi:
        #print("            Replacing: " + ">" + str(x[0]) + "<",">" + str(x[1]) + "<" )
        contents = contents.replace(">" + str(x[0]) + "<",">" + str(x[1]) + "<")
    

    f = open(outFile,"w+")
    f.write(contents)
    f.close
                                                        
def toPDF(inFile, outFile):
    executeString = "inkscape.exe --export-filename=\"" + outFile + "\" \"" + inFile + "\""
    #print("                Executing: " + executeString)
    subprocess.call(executeString)
    


    

    
    



    
