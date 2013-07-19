##Information on this folder..##

There are three types of files here in two broad categories:
* items that define "Designs":
    *  Something.svg : The actual svg components that get layered up to make a keyguard
    *  Something.xml : A small config file that specifies a design. May contain several images and explains how the images are laid out
* items that define "Types" of devices:
    *  Type\_DeviceName.xml : Defines "Types" of guides for different devices
    *  Type\_DeviceName.svg : Defines the image for a type

###Designs###

* Images are the "bits" for keyguards.
* Each thing that can get added to a keyguard has to have a small XML file.  A xml file looks like this:

        <design>
            <name>GoTalk 16</name>
            <type>ipad</type>
            <case>fullscreen</case>
            <image source="GoTalk-16.svg" position="60,90" id="GoTalk16"/>
            <image source="GoTalk-Nav.svg" position="57,44" id="GoTalkNav"/>
        </design>

Lets break this down..

    <design>
     
* You need this. Note the other type of xml file is for "Types"

    <name>GoTalk 16</name>

* What's the name of this file? What does it layout?
    
         <type>ipad</type>

* What was it designed for (relates to Type file)
    
        <case>fullscreen</case>

* Which case was it designed for?
    
        <image source="GoTalk-16.svg" position="60,90" id="GoTalk16"/>

* Name the image. Each image MUST have:
    * source = the name of the file (and must be SVG)
    * position = x,y co-ordinates (from Top Left) where it should be placed
    * id = not needed but maybe useful in the future..
    
            <image source="GoTalk-Nav.svg" position="57,44" id="GoTalkNav"/>

* Note you can put multiple images in one design. 
    
        </design>

* You need this or horrible things will happen!

###Types###

* Type Images start with "Type_" 
* Each Type of device is described by a small xml file. It looks like this:

        <type>
            <name>iPad</name>
            <width>238mm</width>
            <height>182mm</height>
            <image source="Type_iPadOutline.svg" position="0,0"/>
        </type>
    
Note the main thing is width and height. This will define the size of the image that gets finally composed. 