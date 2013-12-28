function getParameterDefinitions() {
  return [
    { name: 'outerWidth', type: 'float', initial: 238, caption: "Outer width of the guard:" },
    { name: 'outerHeight', type: 'float', initial: 182, caption: "Outer height of the guard:" },
{ name: 'screenWidth', type: 'float', initial: 198, caption: "Screen width of the guard:" },    { name: 'screenHeight', type: 'float', initial: 148, caption: "Screen height of the guard:" },    
{ name: 'rounded', type: 'choice', caption: 'Round the corners?', values: [0, 1], captions: ["No thanks", "Yes please"], initial: 1 },
{ name: 'cellSpacing', type: 'float', caption: 'What is the cell spacing (in mm)?', initial:4},
{ name: 'cellWidth', type: 'float', caption: 'What is the number of cells along?', initial:4},
{ name: 'cellHeight', type: 'float', caption: 'What is the number of cells high?', initial:4},    
{ name: 'depth', type: 'float', initial: 7, caption: "Depth of the guard:" },
 { name: 'guardstartx', type: 'float', initial: 20, caption: "Where does the screenstart (x - along - mm):" },
 { name: 'guardstarty', type: 'float', initial: 17, caption: "Where does the screenstart (y - up - mm):" }];
 }

function main(params) {

    if(params.rounded == 1) {
        return CAG.roundedRectangle({center: [params.outerWidth/2,params.outerHeight/2], radius: [params.outerWidth/2,params.outerHeight/2, params.depth], roundradius: 4, resolution: 8}).subtract(translate([params.guardstartx+20,params.guardstarty+20,10],
                         createGrid(params.screenWidth,
                         params.screenHeight,
                         params.cellWidth,
                         params.cellHeight,
                         params.cellSpacing, params.rounded) 
                         )
                        ).extrude({offset: [0,0,params.depth]});
    } else {
      return square({size: [params.outerWidth,params.outerHeight]}).subtract(translate([params.guardstartx,params.guardstarty,10],
                         createGrid(params.screenWidth,
                         params.screenHeight,
                         params.cellWidth,
                         params.cellHeight,
                         params.cellSpacing, params.rounded) 
                         )
                        ).extrude({offset: [0,0,params.depth]});
                    
    }                   
}


function createGrid(w, h, x, y, cellspacing, rounded) {
    cellwidth = (w-(cellspacing*x))/x;
    cellheight = (h-(cellspacing*y))/y;
    var squares = [];

    i = 0;
    for(xi = 0; xi < x; xi++){
        for (yi = 0; yi < y; yi++) { 
                posx = ((cellwidth+cellspacing)*xi)+cellspacing;
                posy = ((cellheight+cellspacing)*yi)+cellspacing;
                
                    if (rounded ==1 ) { 
                        squares[i] = CAG.roundedRectangle({center: [posx,posy], radius: [cellwidth/2, cellheight/2], roundradius: 1, resolution: 4});
                    } else {
                        squares[i] = translate([posx,posy,0], square([cellwidth,cellheight]));
                    }
                
                
                i++;
        }
    }
    return squares;
}
