<?php

ini_set('error_reporting', E_ALL);
ini_set ( "display_errors", "1");
ini_set ( "display_startup_errors", "1");
ini_set ( "html_errors", "1");
ini_set ( "docref_root", "http://www.php.net/");
ini_set ( "error_prepend_string", "<div style='color:red; font-family:verdana; border:1px solid red; padding:5px;'>");
ini_set ( "error_append_string", "</div>");

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

#./GridCreator.py --cellwidth 7 --cellheight 5 --winwidth 198 --winhight 148 --cellspacing 1.705"
    $cmd = 'GridTemplater.py ';
    if (is_int($_POST['cellwidth'])){
        $cmd.='--cellwidth '.$_POST['cellwidth'].' ';
    } 
    
    if (is_int($_POST['cellheight'])){
        $cmd.='--cellheight '.$_POST['cellheight'].' ';
    } 

    if (is_int($_POST['winhight'])){
        $cmd.='--winheight '.$_POST['winhight'].' ';
    } 

    if (is_int($_POST['winwidth'])){
        $cmd.='--winwidth '.$_POST['winwidth'].' ';
    } 

    if (is_int($_POST['cellspacing'])){
        $cmd.='--cellspacing '.$_POST['cellspacing'].' ';
    } 
    
    $fname = realpath('createddesigns/').'/'.get_random_string('abcdefghijklmnopqrstuvwxyz018', 6).'-template';    
    //Parse the script output
    $cmd.= '-f '.$fname;
    $path = "/usr/bin/python ".realpath('../').'/'.$cmd;
    shell_exec($path);
    
    
    if (file_exists($fname.'.svg')){
        header('Content-disposition: attachment; filename=KeyGuideTemplate.svg');
        header('Content-type: image/svg+xml');
        echo file_get_contents($fname.'.svg');
        unlink($fname.'.svg');
        exit();
    } else {
        echo "Sorry. Something went wrong\n<br \>";
        echo $path;
    }
}
?>