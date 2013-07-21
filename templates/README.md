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
            <type>iPad</type>
            <case>fullscreen</case>
            <image source="GoTalk-16.svg" position="60,90" id="GoTalk16"/>
            <image source="GoTalk-Nav.svg" position="57,44" id="GoTalkNav"/>
        </design>

Lets break this down..

        <design>
     
* You need this. Note the other type of xml file is for "Types"

        <name>GoTalk 16</name>

* What's the name of this file? What does it layout?
    
        <type>iPad</type>

* What was it designed for (relates to Type file) NB: Must be exactly the same as one of the types. This is case sensitive. 
    
        <case>fullscreen</case>

* Which case was it designed for? (NB: This isn't used as yet)
    
        <image source="GoTalk-16.svg" position="60,90" id="GoTalk16"/>

* Name the image. Each image MUST have:
    - source = the name of the file (and must be SVG)
    - position = x,y co-ordinates (from Top Left) where it should be placed. This is in pixels (with no letters behind the numbers as above) or mm. e.g. 10mm,10mm would move it 10mm in and 10mm down. NB: Must have no spaces in between
    - id = not needed but maybe useful in the future..

* Note you can put multiple images in one design (GoTalk-Nav.svg for example). This is how you "stack" components into one. This means you can create a design with one or multiple elements. It allows for a heap of flexibility. 
    
        </design>

* You need this final line or horrible things will happen!

###Types###

So these define the different types of devices the keyguides are made for.

* Type xml files start with "Type\_" e.g. "Type\_NAME.xml"
* This small xml file should look like this:

        <type>
            <name>iPad</name>
            <width>238mm</width>
            <height>182mm</height>
            <image source="Type_iPadOutline.svg" position="0,0"/>
            <optionals>iPadHomeButton,iPadMagnets,iPadSuckers</optionals>
        </type>
    
Note the main thing is width and height. This will define the size of the image that gets finally composed.  The other thing to note is "optionals". This is a comma seperated list of "designs" that can be optional for this device. Think buttons and attachment methods. 