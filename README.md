#KeyGuideMaker#

This is a collection of KeyGuide components. It includes:

* a line command tool (KeyGuideMaker.py) to help compose keyguides from a number of images (SVG files)
* [a web front end](html/) (you can see a live version of this [here](http://keyguides.sourceymonkey.com))
* [a directory of keyguide templates](/templates) and [a syntax for creating them (XML files with SVG)](/templates#readme)

We also have a directory of ready-compiled, ready-to-print designs that need no tool to get going with. (YET TO BE INCLUDED)

##Credits##

Simon Judge and Will Wade wrote this with some testing and support from Marie.
Thanks to [Fablab Manchester](http://www.fablabmanchester.org) for helping to cut and trial Simon and Marie's designs.

#KeyGuideMaker.py#

This is a line command tool to combine multiple SVG elements into one. It allows for the most flexibility. 

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
      -h, --help            
                            show this help message and exit
      
      --type TYPE, -t TYPE  
                            What device are these for? iPad, iPadMini, Powerbox?
      
      --designs DESIGNS, -d DESIGNS
                            list the name of the designs you want to convert to a guide.
                              NB: uses the filenames of the XML files
      
      --output OUTPUT, -o OUTPUT
                            Not working. EPS, SVG, PDF, PS
      
      --filename FILENAME, -f FILENAME
                            Name of the final keyguide image that gets created
      
      --formachine FORMACHINE, -m FORMACHINE
                            Change the format of the file ready for a particular machine.
                              e.g ponoko or razorlab need blue instead of black.
      
      --version             Get version number
      
For example: To make a keyguide of TouchChat-80 with a home button and some suckers for attachment, called "TouchChatKeyGuide.svg" and ready it for [Ponoko](https://www.ponoko.com) (who use blue lines for cutting) use:

    ./KeyGuideMaker.py -t iPad -d "TouchChat-80,iPadHomeButton,iPadSuckers" -f TouchChatKeyGuide
    
For a list of ready available components to add to your keyguide look at the [templates directory](templates/). 

##Licence##

![CC-A](http://i.creativecommons.org/l/by/3.0/88x31.png)
This is part of the Open Assistive Technology Initiative. That means it conforms to [CC-BY (Creative Commons Attribution)](http://creativecommons.org/licenses/by/3.0). 