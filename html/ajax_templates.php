<?php
error_reporting(E_ALL);


if($_POST['id']){
    $id=$_POST['id'];
    
    if ($id==1){
        $templates = 'db/TypeiPad.csv';
    } elseif ($id==2){
        $templates = 'db/TypeiPadMini.csv';
    } elseif ($id==3){
       $templates = 'db/TypePowerbox.csv';
    }

    $row=1;
    if (($handle = fopen($templates, "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            if($row == 1){ $row++; continue; }
            $row++;
            echo '<option value="'.$data[0].'">'.$data[1].'</option>';
        }
        fclose($handle);
    }

}
?>