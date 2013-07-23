#!/usr/bin/env python

"""
    Allows you to create a keyguide/guard
    
    # run with 
    -type -designs (csv) -output -formachine 
    
    # To turn this into a binary
    python pyinstaller.py -F -w KeyGuideMaker.py
    (w for windowless version)
"""

import argparse
import logging
import os
# Needs https://github.com/btel/svg_utils
try:
    import svgutils.transform as sg
except ImportError:
    print "SVG_UTILS needs to be downloaded and installed from https://github.com/btel/svg_utils"
import sys 
# for the XML parsing cETree is faster
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
# call with
# -type -designs (comma seperated list of designs)
# and it outputs a final svg 
# use -output to change the output from svg to pdf, png
# use -formachine to change machine details for laser cutter

# Simply adds a layout to a design

def addLayout(design,images):
    tree = ET.parse(__location__+"/templates/"+design+".xml").getroot()
    # All the following aren't actually needed.. yet!
    #name= tree.findtext("name")
    #type= tree.findtext("type")
    #case= tree.findtext("case")
    # for each layout..
    for image in tree.findall('image'):
        isource = image.get("source")
        ipos = image.get("position").split(",")

        img = sg.fromfile(__location__+'/templates/%s' % isource)
        iobj = img.getroot()
        iobj.moveto(ipos[0],ipos[1])
        images.append(iobj)
    return True

def recolourforlab(svg,formachine):
    if formachine=='ponoko' or formachine=='razorlab':
        return svg.replace('#000000','#0000FF')
    else:
        return svg

def createDesign(type, designs, filename="output", output="svg", formachine="epilog-mini"):
    # Whats the type? Lets get the size and basic outline..
    
    tree = ET.parse(__location__+"/templates/Type_"+type+".xml")
    doc = tree.getroot()
    #create new SVG figure - dimensions of iPad
    stackedLayout = sg.SVGFigure(doc.find('width').text, doc.find('height').text)
    #lets add the type layout
    images = []
    addLayout('Type_'+type,images)

    # now add each of the designs    
    for design in designs:
        addLayout(design,images)

    # append plots and labels to figure
    stackedLayout.append(images)
    # save generated SVG files
    if (filename=='stream'):
        print recolourforlab(stackedLayout.to_str(),formachine)
    else:
        data = recolourforlab(stackedLayout.to_str(),formachine)
        if not (filename.endswith('.svg')):
            filename = filename+'.svg'
        svg_file = open(filename, "wb")
        svg_file.write(data)
        svg_file.close()        
        
    
# to define values for comma sep list of values
def csv(value):
    return map(str, value.split(","))

parser = argparse.ArgumentParser(prog='KeyGuideMaker',description='Creates keyguides from xml design files and svgs. Use like: ./KeyGuideMaker.py -t iPad -d "TouchChat-80,iPadHomeButton" -f will')
# Basics
parser.add_argument('--type','-t', type=str, default='ipad', help='What device are these for? iPad, iPadMini, Powerbox?')
parser.add_argument('--designs','-d', type=csv, help='list the name of the designs you want to convert to a guide. NB: uses the filenames of the XML files')
parser.add_argument('--output','-o', type=str, default="SVG", help='Not working. EPS, SVG, PDF, PS')      
parser.add_argument('--filename','-f', type=str, default="output", help='Name of the final keyguide image that gets created')
parser.add_argument('--logfile','-l', type=str, default="", help='Logfile location. NB: If blank no log created')      
parser.add_argument('--formachine','-m', type=str, default="epilog-mini", help='Change the format of the file ready for a particular machine. e.g ponoko or razorlab need blue instead of black.')      
parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
# All the components of a Server request
args = parser.parse_args()

#Fix the location if called elsewhere
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if (args.logfile!=''):
    logging.basicConfig(filename='KeyGuideMaker.log',level=logging.DEBUG)
createDesign(args.type,args.designs,args.filename,args.output,args.formachine)