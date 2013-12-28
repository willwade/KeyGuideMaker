#KeyGuideMaker - SquareDetector v1#

A little app that works out the squares in an image - or set of images. 

##Credits##

kamosion


##Installation:##

* [Python](http://www.python.org/download/releases/2.7.2/)
* [OpenCV 2.x](https://github.com/btel/svg_utils)
* [pygame]
* [easygui] 

NB: EasyGui is modified. Please use the modified version in place of the installed lib file..


##Random notes##

 ['Points Count',[0,100000]], -- points in contour
    ['Rect Proportion',[0.1,10]], - width/height (rectangle which contains this contour)
    ['AreaSquare Koef',[0.1,1]], - "contour area" divide area of rectangle
    ['Area',[0.001,0.9]], -- min and max area of contour in percents of image
    ['Width',[0.01,1]], -- width of square (in percents of image width)
    ['Heigh',[0.01,1]], -- height of square (in percents of image height)
    ['X',[0,1]], - x -- (in percents of image width)
    ['Y',[0,1]], - y -- (in percents of image height)
    ['Out resolution px',[198,148]],
    
    SquareDetect.py run 
    SquareDetect.py setup
    SquareDetect.py
    
##Licence##

![CC-A](http://i.creativecommons.org/l/by/3.0/88x31.png)
This is part of the Open Assistive Technology Initiative. That means it conforms to [CC-BY (Creative Commons Attribution)](http://creativecommons.org/licenses/by/3.0). 