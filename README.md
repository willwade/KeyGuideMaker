#KeyGuideMaker#

This is a collection of KeyGuide components - and a script to help make a keyguide. 

##Installation:##

* [Python](http://www.python.org/download/releases/2.7.2/)
* [svg_utils](https://github.com/btel/svg_utils)
 
In the future you may need some more things... but right now thats it!

You may also want to use [InkScape](http://inkscape.org/) to do any little personal editing after the basic keyguide has been created (e.g. convert to PDF, EPS or change the line thickness for different laser cutting machines)

##Usage##

    /KeyGuideMaker.py -h
    usage: KeyGuideMaker [-h] [--type TYPE] [--designs DESIGNS] [--output OUTPUT]
                         [--filename FILENAME] [--formachine FORMACHINE]
                         [--version]

    Creates keyguides from xml design files and svgs. Use like: /KeyGuideMaker.py
    -t iPad -d "TouchChat-80,iPadHomeButton" -f will

    optional arguments:
      -h, --help            show this help message and exit
      
      --type TYPE, -t TYPE  What device are these for? iPad, iPadMini, Powerbox?
      
      --designs DESIGNS, -d DESIGNS
                            list the name of the designs you want to convert to a
                            guide. NB: uses the filenames of the XML files
      
      --output OUTPUT, -o OUTPUT
                            Not working. EPS, SVG, PDF, PS
      
      --filename FILENAME, -f FILENAME
                            Name of the final keyguide image that gets created
      
      --formachine FORMACHINE, -m FORMACHINE
                            Not Working. Change the format of the file ready for a
                            particular machine
      
      --version             Get version number
      
For example: To make a keyguide of TouchChat-80 with a home button and some suckers for attachment and called "TouchChatKeyGuide.svg":

    /KeyGuideMaker.py -t iPad -d "TouchChat-80,iPadHomeButton,iPadSuckers" -f TouchChatKeyGuide
    
For a list of ready available components to add to your keyguide look at the [templates directory](templates/). 

##Credits##

Simon Judge and Will Wade wrote this with some testing and support from Marie.
