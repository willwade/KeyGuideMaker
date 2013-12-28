// The height of the Acrylic used for the keyguard
acrylicHeight = 3;
width = 25.4;
height = 230;

function main() {
return union( 
    CAG.roundedRectangle({radius: [width/2,height/2, 1], roundradius: 4, resolution: 12}), 
    CAG.roundedRectangle({radius: [(width/2)/2,height/2, acrylicHeight-1], roundradius: 4, resolution: 12}), 
    translate([0,-13.4,acrylicHeight-1], difference(difference(
        CAG.roundedRectangle({radius: [width/2,height/2, 2], roundradius: 5, resolution: 12}),  translate ([10,7,-1], 
        cylinder({r:5,h:2,fn:20})
        ), 
        translate ([25,7,-1], cylinder({r:5,h:2,fn:20})
        ), 
	   translate ([200,7,-1], cylinder({r:5,h:2,fn:20})
        ), 
        translate ([215,7,-1], cylinder({r:5,h:2,fn:20})
        )
    ), 
	translate([33,0,0], CSG.roundedCube({radius: [160, 10, 3], roundradius: 2, resolution: 32})))
    )
    );
}

/*

}

}
*/