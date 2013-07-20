<?php
// this file is used to generate the html page. It doesn't need to be super duper dynamic since the options for each type of device is rarely updated the ajax call is the only bit of php that will get called regularly
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title>
			KeyGuide Creator!
		</title>
		<link rel="stylesheet" type="text/css" href="view.css" media="all" />
        <script type="text/javascript" src="view.js"></script> 
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
        <script type="text/javascript">
        $(document).ready(function(){
            $('.options').hide();
            $(".type").change(function(){
                var id=$(this).val();
                var dataString = 'id='+ id;
                $.ajax({
                    type: "POST",
                    url: "ajax_templates.php",
                    data: dataString,
                    cache: false,
                    success: function(html){
                        $(".templates").html(html);
                        $('.options').hide();
                        $('.Type'+id).show();
                        } 
                });
            });
        });
        </script>
</head>
<body id="main_body">
	<img id="top" src="top.png" alt="">
	<div id="form_container">
		<h1>
			<a>
				Keyguide creator!
			</a>
		</h1>
		<form id="form_670561" class="appnitro" method="post" action="guidecreator.php">
			<div class="form_description">
				<h2>
					KeyGuide Creator
				</h2>
				<p>
Make your keyguide you desire here! Please note that this is very very early beta. Lots of things aren't working! If you are interested in playing around with this more take a look at <a href="https://github.com/willwade/KeyGuideMaker">KeyGuideMaker on GitHub</a> which provides a line command tool to make your own keyguide. Credit for this tool goes to
<a href="https://twitter.com/si_judge">@si_judge</a> and <a href="https://twitter.com/willwade">@willwade</a> and its all under a <a href="https://github.com/willwade/KeyGuideMaker#licence">CC-A licence</a>				</p>
			</div>
			<ul>
				<li id="li_1">
					<label class="description" for="element_1">
						Choose your device
					</label>
					<div>
						<select class="element select medium type" id="type" name="type">
							<option value="" selected="selected">
							</option>
							<option value="1">
								iPad
							</option>
							<option value="2">
								iPad Mini
							</option>
							<option value="3">
								Powerbox
							</option>
						</select>
					</div>
					<p class="guidelines" id="guide_1">
						<small>
							Choose the device you need a guide for
						</small>
					</p>
				</li>
				<li id="li_2">
					<label class="description" for="element_1">
						Choose your app 
					</label>
					<div>					
						<select class="element select medium templates" id="element_1" name="templates">
							<option value="" selected="selected">
							</option>
						</select>
					</div>
					<p class="guidelines" id="guide_1">
						<small>
							Choose the app - or keyguard layout you need
						</small>
					</p>
				</li>
				<li id="li_3">
					<label class="description" for="element_2">
						Choose options (if any)
					</label>
					<?
// yeah I'm lazy. deal with it
$n=0;
$types = array('iPad','iPadMini','Powerbox');
foreach ($types as $type){
$n++; 
?>
					<span class="options Type<?=$n?>">
<?
    if (file_exists('db/'.$type.'Options.csv')){     
        $row = 1;
        if (($handle = fopen('db/'.$type.'Options.csv', "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                if($row == 1){ $row++; continue; }
                $row++;
?>
<input id="element_<?=$row?>" name="Opt_<?=$data[2]?>" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_<?=$row?>">
    <?=$data[1]?>
</label>
<?

            }
            fclose($handle);
        }
  }
?>
					</span>
<?
}
?>
				<p class="guidelines" id="guide_3"><small>Choose the options. Note this is particular to each device. If you are trying to find variants on each design see the dropdown. </small></p></li>
				<li class="section_break">
			<h3>Tips!</h3>
			<p>Once downloaded you need to send this to your local laser printing service or your helpful AT company. Note that guides work best between 2mm and 3mm thickness. 6mm is quite chunky and can be tricky with small cell apps. You may need to purchase some acrylic for example these folks sell it pretty cheaply in the UK. Card, leather and all sorts of other materials can be used. We only ask you feedback your results to us so we can improve the designs!</p>
		</li>
<?
/*				
				<li id="li_4" >
		<label class="description" for="element_4">Choose your format </label>
		<div>
		<select class="element select medium" id="format" name="format"> 
			<option value="" selected="selected"></option>
<option value="svg" selected>SVG</option>
<option value="pdf" >PDF</option>
<option value="png" >PNG</option>
<option value="jpeg" >JPEG</option>
		</select>
		</div><p class="guidelines" id="guide_4"><small>Note that SVG is editable. The rest aren't so easy to edit!</small></p> 
		</li>
*/ ?>				
				<li class="buttons">
					<input type="hidden" name="form_id" value="670561" />
					<input id="saveForm" class="button_text" type="submit" name="submit" value="Download" />
				</li>
			</ul>
		</form>
		<div id="footer">
		</div>
	</div>
	<img id="bottom" src="bottom.png" alt="" />
</body>
</html>
