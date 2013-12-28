//Outer Width and height
ow=238;
oh=182;

//Screen Width and height
sw=198;
sh=148;

//Where does screen start?
sx = 20;
sy = 17;

// cells wide
cw = 5;
// cells high
ch = 4;
// cell spacing in mm
cs = 4;
// cells to bind
bindfrom = [[2,2]];
bindto = [[2,4]];

$fn=50;

//to counter the minkowski affect
translate([10,10,0]){
    difference(){
        hull()
        {
         square([ow,oh]);
         circle(r=10);
        }
        translate([sx,sy,0]){
            createGrid(sw,sh,cw,ch,cs);
        }
    }
}
// W = width of entire block
// h = height of block
// x = number of cells along (w)
// y = number of cells up (h)

module createGrid(w, h, x, y, cellspacing) {
cellwidth = (w-(cellspacing*x))/x;
cellheight = (h-(cellspacing*y))/y;
n = 1; 
    for (xi = [0:x-1]) { 
        for (yi = [0:y-1]) { 
            echo (xi);
                assign (posx = ((cellwidth+cellspacing)*xi)+cellspacing, posy = ((cellheight+cellspacing)*yi)+cellspacing) {
                translate([posx,posy,0]) square([cellwidth,cellheight]);
                }
        }
    }
}