$fn = 100;
cube([123,25.4,1]);

difference(){
translate([20,10,0]){
	rotate(a=[0,90,90]) {
		difference() {
		cylinder(h=25.4,r=10);
		translate([-6,0,6]) cylinder(h=20,r=5);
		}
	}
}

translate([10,9,-10]){
cube([22,27,10]);
}
}