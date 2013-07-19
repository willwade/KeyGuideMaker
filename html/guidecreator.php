<?php
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

    //Parse the script output
    $cmd='KeyGuideMaker.py -t '.$type.' -d '.'"'.$opts.'" -f stream';
    
    header('Content-disposition: attachment; filename=KeyGuide.svg');
    header('Content-type: image/svg+xml');
    print shell_exec("python ../".$cmd);
    exit();
}
?>