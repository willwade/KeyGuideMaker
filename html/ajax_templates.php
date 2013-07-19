<?php
error_reporting(E_ALL);


if($_POST['id']){
    $id=$_POST['id'];
    
    if ($id==1){
        $templates = 'iPad.csv';
    } elseif ($id==2){
        $templates = 'iPadMini.csv';
    } elseif ($id==3){
       $templates = 'Powerbox.csv';
    }

    $row=0;
    if (($handle = fopen($templates, "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            echo '<option value="'.$data[0].'">'.$data[1].'</option>';
            $row++;
        }
        fclose($handle);
    }

}
?>