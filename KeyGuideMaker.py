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
    print "SVG_UTILS needs to be downloaded \
        and installed from https://github.com/btel/svg_utils"
#for the XML parsing cETree is faster
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
def add_layout(templatedir, design, images):
    """Add layout
       Add a layout to the overall design. 
        Takes a XML template file
    """
    design_file = get_file(templatedir, design+".xml")
    if (design_file):
        tree = ET.parse(design_file).getroot()
        # NB: Images are assumed to be at the same
        #     directory path of the xml file
        for image in tree.findall('image'):
            isource = image.get("source")
            ipos = image.get("position").split(",")
            img = sg.fromfile(os.path.dirname(design_file)+'/'+isource)
            iobj = img.getroot()
            iobj.moveto(ipos[0], ipos[1])
            images.append(iobj)
        return True
    else:
        return False

def recolour_for_lab(svg, formachine):
    """Recolour for lab
        Simply changes the colour of anything (not only lines) from one hex colour to another
    """
    if formachine == 'ponoko' or formachine == 'razorlab':
        return svg.replace('#000000', '#0000FF')
    else:
        return svg

def get_file(dirs, file):
    """Get file
        Only needed in the latest versions which allow for multiple template directories to be provided
    """
    for dir in dirs:
        if os.path.isdir(dir):
            listing = os.listdir(dir)
            for infile in listing:
                if (file == infile):
                    return dir+'/'+file
    return False

def create_design(type, templatedir, designs, filename="output",
                         output="svg", formachine="epilog-mini"):
    """create_design
        This is really the _main_ function. Lays one set of images over another
    """
    # now get a list of template directories
    templatedir.append(__location__+'/templates/')

    # Whats the type? Lets get the size and basic outline..
    type_file = get_file(templatedir, "Type_"+type+".xml")
    if(type_file):
        tree = ET.parse(type_file)
        doc = tree.getroot()
        #create new SVG figure - dimensions of iPad
        stacked_layout = sg.SVGFigure(doc.find('width').text,
                                     doc.find('height').text)
        #lets add the type layout
        images = []
        add_layout(templatedir, 'Type_'+type, images)

        # now add each of the designs
        for design in designs:
            add_layout(templatedir, design, images)

        # append plots and labels to figure
        stacked_layout.append(images)
        # save generated SVG files
        if (filename=='stream'):
            print recolour_for_lab(stacked_layout.to_str(), formachine)
        else:
            data = recolour_for_lab(stacked_layout.to_str(), formachine)
            if not (filename.endswith('.svg')):
                filename = filename+'.svg'
            svg_file = open(filename, "wb")
            svg_file.write(data)
            svg_file.close()
    else:
        return 'Error. No Type file found'

# to define values for comma sep list of values
def csv(value):
    """Simply maps a csv field to a list"""
    return map(str, value.split(","))

parser = argparse.ArgumentParser(prog = 'KeyGuideMaker', description =
                'Creates keyguides from xml design files and svgs.Use like:\
                ./KeyGuideMaker.py -t iPad -d "TouchChat-80,\
                      iPadHomeButton" -f will')
# Basics
parser.add_argument('--type', '-t', type=str, default='ipad', help='What device are these for? iPad, iPadMini, Powerbox?')
parser.add_argument('--designs', '-d', type=csv, help='list the name of the designs you want to convert to a guide. NB: uses the filenames of the XML files')
parser.add_argument('--output', '-o', type=str, default="SVG", help='Not working. EPS, SVG, PDF, PS')
parser.add_argument('--filename', '-f', type=str, default="output", help='Name of the final keyguide image that gets created')
parser.add_argument('--logfile', '-l', type=str, default="", help='Logfile location. NB: If blank no log created')
parser.add_argument('--formachine', '-m', type=str, default="epilog-mini", help='Change the format of the file ready for a particular machine. e.g ponoko or razorlab need blue instead of black.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
parser.add_argument('--templatedirs', '-p', type=csv, default='', help='Provide additional directories to search for templates')

# All the components of a Server request
args = parser.parse_args()

#Fix the location if called elsewhere
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if (args.logfile!=''):
    logging.basicConfig(filename='KeyGuideMaker.log', level=logging.DEBUG)
create_design(args.type, args.templatedirs, args.designs, args.filename, args.output, args.formachine)
