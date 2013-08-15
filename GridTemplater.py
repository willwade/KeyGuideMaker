#!/usr/bin/env python

"""GridTemplater

Usage: GridTemplater [-h] 
                     [--cellwidth CELLWIDTH] [--cellheight CELLHEIGHT]
                     [--type TYPE] 
                     [--winwidth WINWIDTH] [--winheight WINHEIGHT] [--dpi DPI]
                     [--cellspacing CELLSPACING] [--spacingunits SPACINGUNITS]
                     [--linewidth LINEWIDTH] [--rxy RXY] [--filename FILENAME]
                     [--logfile LOGFILE] [--version]

Creates bases of keyguard designs from some basic settings. 

optional arguments:
  -h, --help            show this help message and exit
  --cellwidth CELLWIDTH
                        The number of cells across
  --type TYPE, -t TYPE  Provide a device type and you don't need to provide
                        winwidth, winheight or dpi
  --cellheight CELLHEIGHT
                        The number of cells up
  --winwidth WINWIDTH   The width of the aperture (window) in mm
  --winheight WINHEIGHT
                        The height of the aperture (window) in mm
  --dpi DPI, -d DPI     Dots per inch. DPI [default: 132]
  --cellspacing CELLSPACING, -s CELLSPACING
                        Cell Spacing [default: 8]
  --spacingunits SPACINGUNITS, -u SPACINGUNITS
                        Cell Spacing units (px or mm) [default: px]
  --linewidth LINEWIDTH
                        Width of the lines to draw (in mm) [default: 0.01]
  --rxy RXY             The curvature of the rectangles [default: 4]
  --filename FILENAME, -f FILENAME
                        Name of the final image that gets created [default: output]
  --logfile LOGFILE, -l LOGFILE
                        Logfile location. NB: If blank no log created
  --version             Get version number

"""
import logging
import os
import sys
# Needs https://pypi.python.org/pypi/svgwrite/
try:
    import svgwrite
except ImportError:
    print "svgwrite needs to be installed. See https://pypi.python.org/pypi/svgwrite/"
try:
    from docopt import docopt
except ImportError:
    print "you need to install docopt. See https://github.com/docopt/docopt"

# for the XML parsing cETree is faster
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def convertpxtomm(pixels, dpi=132):
     #first convert mm to inch
     spixels_mm=(float(pixels)*25.4)/dpi
     return spixels_mm

def getDeviceDetails(type):
    tree = ET.parse(__location__+"/templates/Type_"+type+".xml")
    doc = tree.getroot()
    return {'winwidth':int(doc.find('winwidth').text), 'winheight':int(doc.find('winheight').text) ,'dpi': int(doc.find('dpi').text)}  


def createGrid(type,w,h,x,y,cellspacing=8,spacingunits='px',rxy=4,fname='output',linewidth=0.01,dpi=132):
    # ok lets do some math!
    # whats the cell spacing? NB: this is mm - in the grid its pixels so  this needs converting
    #cellspacing = convertpxtomm(8,264)
    if spacingunits == 'px':
        cellspacing_mm = convertpxtomm(cellspacing,dpi)
    else:
        cellspacing_mm = float(cellspacing)
    
    # print 'cellspacing_mm', cellspacing_mm, 'w:', w, 'h:',h, 'x:', x, 'y:', y
    
    cellwidth = ((float(w)-(cellspacing_mm*int(x)))/int(x))
    cellheight = ((float(h)-(cellspacing_mm*int(y)))/int(y))
    #print 'cellspacing', cellspacing, 'width', cellwidth, 'height', cellheight
    #nb: cellspacing is pixels - but needs to be converted
    
    dwg = svgwrite.Drawing(filename = fname+".svg", size = (str(w)+"mm", str(h)+"mm"))
    # lets work out all the x, y points for each cell.
    # sure there is a better way of doing this
    colpos = list()
#    colpos.append(cellspacing)
    rowpos = list()
#    rowpos.append(cellspacing)
    for l in (range(int(x))):
        startdrawx = ((cellwidth+cellspacing_mm)*l)+cellspacing_mm
        colpos.append(startdrawx)

    for h in (range(int(y))):
        startdrawy = ((cellheight+cellspacing_mm)*h)+cellspacing_mm
        rowpos.append(startdrawy)

    for x in colpos:
        for y in rowpos:
            dwg.add(dwg.rect(insert = (str(x)+"mm", str(y)+"mm"), 
                size = (str(cellwidth)+"mm", str(cellheight)+"mm"), 
                stroke_width = "0.01mm", 
                stroke = "black",  
                fill = "none", 
                rx = (rxy), ry = (rxy)))

    #print(dwg.tostring())
    dwg.save()
    
# ./GridTemplater.py --cellwidth 7 --cellheight 5 --winwidth 198 --winheight 148 --cellspacing 1.705  or ./GridTemplater.py --type iPad --cellwidth 7 --cellheight 5 --cellspacing 8 -u px

if __name__ == '__main__':
    arguments = docopt(__doc__, version='GridTemplater vb1')
    print arguments
    #Fix the location if called elsewhere
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if arguments['--type'] !=None:
        typedets = getDeviceDetails(arguments['--type'])
        arguments['--dpi'] = typedets['dpi']
        arguments['--winwidth'] = typedets['winwidth']
        arguments['--winheight'] = typedets['winheight']

# here we go. This is a monster    
createGrid(arguments['--type'],arguments['--winwidth'],arguments['--winheight'],arguments['--cellwidth'],arguments['--cellheight'],arguments['--cellspacing'],arguments['--spacingunits'],arguments['--rxy'], arguments['--filename'],arguments['--linewidth'],arguments['--dpi'])