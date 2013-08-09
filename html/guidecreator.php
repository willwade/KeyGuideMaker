<?php

ini_set('error_reporting', E_NOTICE);
ini_set ( "display_errors", "1");
ini_set ( "display_startup_errors", "1");
ini_set ( "html_errors", "1");
ini_set ( "docref_root", "http://www.php.net/");
ini_set ( "error_prepend_string", "<div style='color:red; font-family:verdana; border:1px solid red; padding:5px;'>");
ini_set ( "error_append_string", "</div>");

function unlinkFiles($files){
    foreach($files as $file){
        @unlink($file);
    }
}

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
    
    #lets grab any file uploaded and the window position..
    $files_to_delete = array();
    $newtemp = '';
    if(array_key_exists('usefile',$_POST)){
        $ext = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
        if (trim($_FILES['file']['type']) == 'image/svg+xml'){
            $target_path = realpath('createddesigns/');
            $target_name = get_random_string('abcdefghijklmnopqrstuvwxyz018', 6).'.svg';
            $target_file = $target_path .'/'.$target_name ;
            if(move_uploaded_file($_FILES['file']['tmp_name'], $target_file)) {
                array_push($files_to_delete, $target_file);
                #echo "The file ".  basename( $_FILES['file']['name'])." has been uploaded";
                #now create the design.xml file
                $template = file_get_contents($target_path.'/template.xml');
                $template = str_replace("%n", 'temp', $template);
                $template = str_replace("%t", $type, $template);
                # remember its always alongside the xml file. dats de rulez
                $template = str_replace("%src", $target_name, $template);
                $template = str_replace("%x", $_POST['xpos'], $template);
                $template = str_replace("%y", $_POST['ypos'], $template);
                $newtfile = get_random_string('abcdefghijklmnopqrstuvwxyz018', 6);
                $newtemp = $target_path.'/'.$newtfile.'.xml';
                file_put_contents($newtemp, $template);
                array_push($files_to_delete, $newtemp);
                $opts.=$newtfile.',';
            } else {
                die("There was an error uploading the file, please try again!");
            }
        } else {
            die("You need to upload an SVG file");
        }
    }
    
    //lazy approach to strip last comma
    $opts = substr($opts, 0, -1);
    # now do the stacking. NB: always svg
    $fname = realpath('createddesigns/').'/'.get_random_string('abcdefghijklmnopqrstuvwxyz018', 6).'-guide.svg';
    array_push($files_to_delete, $fname);    
    //Parse the script output
    $cmdtemps = ($newtemp == '' ? '' : ' -p '.$target_path);
    $cmd='KeyGuideMaker.py -t '.$type.' -d '.'"'.$opts.'" -f '.$fname.' -m'.$_POST['formachine'].$cmdtemps;
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
        array_push($files_to_delete, $fnamebeforesvg.'.svg');
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
        unlinkFiles($files_to_delete);
        exit();
    } else {
        echo "Sorry. Something went wrong\n<br \>";
        print_r($_POST);
        echo "cmd:".$cmd."<br/>";
        echo "fname:".$fname."<br/>";
        echo "convertcmd:".$convertcmd."<br/>";
        unlinkFiles($files_to_delete);
    }
}
?>