#!/usr/bin/env python

"""
    Allows you to create a svg file with a fixed number of squares
    
    # run with 
    -curved -x (number along) -y (number high)  
"""

import argparse
import logging
import os
import sys
# Needs https://pypi.python.org/pypi/svgwrite/
try:
    import svgwrite
except ImportError:
    print "svgwrite needs to be installed. See https://pypi.python.org/pypi/svgwrite/"

# for the XML parsing cETree is faster
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def convertpxtomm(pixels,dpi):
     #first convert mm to inch
     spixels_mm=(pixels*25.4)/dpi
     return spixels_mm

def getDeviceDetails(type):
    tree = ET.parse(__location__+"/templates/Type_"+type+".xml")
    doc = tree.getroot()
    return {'winwidth':int(doc.find('winwidth').text), 'winheight':int(doc.find('winheight').text) ,'dpi': int(doc.find('dpi').text)}  


def createGrid(type,dpi,w,h,cellspacing,spacingunits,x,y,linewidth,fname='output',linecurved=True):
    # ok lets do some math!
    # whats the cell spacing? NB: this is mm - in the grid its pixels so  this needs converting
    #cellspacing = convertpxtomm(8,264)
    # line width of the laser cutter
    linewidth = 0.01
    if spacingunits == 'px':
        cellspacing_mm = convertpxtomm(cellspacing,132)
    else:
        cellspacing_mm = cellspacing
    
    # print 'cellspacing_mm', cellspacing_mm, 'w:', w, 'h:',h, 'x:', x, 'y:', y
    
    cellwidth = ((w-(cellspacing_mm*x))/x)
    cellheight = ((h-(cellspacing_mm*y))/y)
    #print 'cellspacing', cellspacing, 'width', cellwidth, 'height', cellheight
    #nb: cellspacing is pixels - but needs to be coonverted
    
    dwg = svgwrite.Drawing(filename = fname+".svg", size = (str(w)+"mm", str(h)+"mm"))
    # lets work out all the x, y points for each cell.
    # sure there is a better way of doing this
    colpos = list()
#    colpos.append(cellspacing)
    rowpos = list()
#    rowpos.append(cellspacing)
    for l in (range(x)):
        startdrawx= ((cellwidth+cellspacing_mm)*l)+cellspacing_mm
        colpos.append(startdrawx)

    for h in (range(y)):
        startdrawy= ((cellheight+cellspacing_mm)*h)+cellspacing_mm
        rowpos.append(startdrawy)

    for x in colpos:
        for y in rowpos:
            dwg.add(dwg.rect(insert = (str(x)+"mm", str(y)+"mm"), 
                size = (str(cellwidth)+"mm", str(cellheight)+"mm"), 
                stroke_width = "0.01mm", 
                stroke = "black",  
                fill = "none", 
                rx = ("4"), ry = ("4")))

    #print(dwg.tostring())
    dwg.save()
    

parser = argparse.ArgumentParser(prog='GridTemplater',description="Creates bases of keyguard designs from some basic settings. Use like: ./GridTemplater.py --cellwidth 7 --cellheight 5 --winwidth 198 --winheight 148 --cellspacing 1.705  or ./GridTemplater.py --type iPad --cellwidth 7 --cellheight 5 --cellspacing 8 -u px")
# Basics
parser.add_argument('--curved','-c', type=bool, default=True, help='Do you want curved guide holes?')
parser.add_argument('--cellwidth', type=int, help='The number of cells across')
parser.add_argument('--type', '-t', type=str, default='', help='Provide a device type and you don\'t need to provide winwidth, winheight or dpi')
parser.add_argument('--cellheight', type=int, default=5, help='The number of cells up')
parser.add_argument('--winwidth', type=int, help='The width of the aperture (window) in mm')
parser.add_argument('--winheight', type=int, help='The height of the aperture (window) in mm')
parser.add_argument('--dpi','-d', type=int, help='Dots per inch. DPI')
parser.add_argument('--cellspacing','-s', type=float, default=8, help='Cell Spacing (in pixels)')
parser.add_argument('--spacingunits','-u', type=str, default='px', help='Cell Spacing units (px or mm)')
parser.add_argument('--linewidth', type=float, default=0.01, help='Width of the lines to draw (in mm)')
parser.add_argument('--filename','-f', type=str, default="output", help='Name of the final  image that gets created')
parser.add_argument('--logfile','-l', type=str, default="", help='Logfile location. NB: If blank no log created')      
parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
# All the components of a Server request
args = parser.parse_args()

#Fix the location if called elsewhere
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if args.type !='':
    typedets = getDeviceDetails(args.type)
    args.dpi = typedets['dpi']
    args.winwidth = typedets['winwidth']
    args.winheight = typedets['winheight']

# here we go. This is a monster    
createGrid(args.type,args.dpi,args.winwidth,args.winheight,args.cellspacing,args.spacingunits,args.cellwidth,args.cellheight,args.linewidth,args.filename,args.curved)