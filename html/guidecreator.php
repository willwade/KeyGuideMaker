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
    if ($_POST['type']==1){
        $templates = 'db/TypeiPad.csv';
        $type = 'iPad';
    } elseif ($_POST['type']==2){
        $templates = 'db/TypeiPadMini.csv';
        $type = 'iPadMini';
    } elseif ($_POST['type']==3){
        $templates = 'db/TypePowerbox.csv';
        $type = 'Powerbox';
    }
    // look up the template    
    $row=0;
    if (($handle = fopen($templates, "r")) !== FALSE) {
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
    #change the colour?
    
    
    //lazy approach to strip last comma
    $opts = substr($opts, 0, -1);
    # now do the stacking. NB: always svg
    $fname = realpath('createddesigns/').'/'.get_random_string('abcdefghijklmnopqrstuvwxyz018', 6).'-guide.svg';    
    //Parse the script output
    $cmd='KeyGuideMaker.py -t '.$type.' -d '.'"'.$opts.'" -f '.$fname.' -m'.$_POST['formachine'];
    $path = "/usr/bin/python ".realpath('../').'/'.$cmd;
    shell_exec($path);
    
    # nb: to change the file format..
    # nb nb: only works with uniconvertor.. and the servers version hasn't got ruddy svg installed
    # install with sudo apt-get install python-uniconvertor
    if($_POST['format']!='svg'){
        $fnamebeforesvg = substr($fname,0,-4);
        $convertcmd = '/usr/bin/uniconvertor '.$fname.' '.$fnamebeforesvg.'.'.$_POST['format'];
        shell_exec($convertcmd);
        $fname = $fnamebeforesvg.'.'.$_POST['format'];
        unlink($fnamebeforesvg.'.svg');
    }
    
    if (file_exists($fname)){
        header('Content-disposition: attachment; filename=KeyGuide-'.$template.'.'.$_POST['format']);
        if ($_POST['format']=='svg'){
            header('Content-type: image/svg+xml');
        } elseif($_POST['format']=='ai'){
            header('Content-Type: application/postscript');
        } elseif($_POST['format']=='wmf'){
            header('Content-Type: image/wmf');
        } elseif($_POST['format']=='ps'){
            header('Content-Type: application/postscript');
        } elseif($_POST['format']=='pdf') {
            header('Content-Type: application/pdf');
        }
        echo file_get_contents($fname);
        unlink($fname);
        exit();
    } else {
        echo "Sorry. Something went wrong\n<br \>";
        print_r($_POST);
        echo "fname:".$fname."<br/>";
        echo "convertcmd:".$convertcmd."<br/>";
    }
}
?>