<?php
function get_random_string($valid_chars, $length)
{
    // start with an empty random string
    $random_string = "";
    // count the number of chars in the valid chars string so we know how many choices we have
    $num_valid_chars = strlen($valid_chars);
    // repeat the steps until we've created a string of the right length
    for ($i = 0; $i < $length; $i++)
    {
        // pick a random number from 1 up to the number of valid chars
        $random_pick = mt_rand(1, $num_valid_chars);
        // take the random character out of the string of valid chars
        // subtract 1 from $random_pick because strings are indexed starting at 0, and we started picking at 1
        $random_char = $valid_chars[$random_pick-1];
        // add the randomly-chosen char onto the end of our string so far
        $random_string .= $random_char;
    }
    // return our finished random string
    return $random_string;
}

if ($_POST){    
    if($_POST['type']==1){
    $type='iPad';
    } elseif ($_POST['type']==2){
    $type='iPadMini';
    } elseif ($_POST['type']==3){
    $type='PowerBox';
    }
    // look up the template    
    $row=0;
    if (($handle = fopen("iPad.csv", "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            if($data[0]==$_POST['templates']){
                $template=$data[2];
            }
            $row++;
        }
        fclose($handle);
    }
    //Lets grab any more BITs
    $opts = $template.',';
    foreach($_POST as $itemk=>$itemv){
        if(substr($itemk,0,4)=='Opt_' && $itemv==1){
            $opts.= substr($itemk,4,strlen($itemk)).',';
        }
    }
    //lazy approach to strip last comma
    $opts = substr($opts, 0, -1);
    
    $fname = realpath('createddesigns/').'/'.get_random_string('abcdefghijklmnopqrstuvwxyz018', 6).'-guide.svg';    
    //Parse the script output
    $cmd='KeyGuideMaker.py -t '.$type.' -d '.'"'.$opts.'" -f '.$fname;
    $path = "/usr/bin/python ".realpath('../').'/'.$cmd;
    print shell_exec($path);

    if (file_exists($fname)){
        header('Content-disposition: attachment; filename=KeyGuide'.$template.'.svg');
        header('Content-type: image/svg+xml');
        echo file_get_contents($fname);
        unlink($fname);
        exit();
    } else {
        echo "Sorry. Something went wrong\n<br \>";
        echo $path;
    }
}
?>