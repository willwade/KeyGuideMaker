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
function evaluate(){
    var item = $(this);
    var relatedItem = $("#" + item.attr("data-related-item")).parent();
    if(item.is(":checked")){
        relatedItem.fadeIn();
    }else{
        relatedItem.fadeOut();   
    }
}

$(document).ready(function(){
    $('input[type="checkbox"]').click(evaluate).each(evaluate);
    $('.options').hide();
    $(".type").change(function(){
        var id=$(this).val();
        var dataString = 'id='+ id;
        $.ajax({
            type: "POST",
            url: "ajax_templates.php",
            data: dataString,
            cache: true,
            success: function(html){
                $(".templates").html(html);
                $('.options').hide();
                $('.Type'+id).show();
                } 
        });
        $.ajax({
            type: "POST",
            url: "ajax_typedets.php",
            data: dataString,
            cache: true,
            success: function(html){
                $(".templates").html(html);
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
		<form id="form_670561" class="appnitro" method="post" action="guidecreator.php" enctype='multipart/form-data'>
			<div class="form_description">
				<h2>
					KeyGuide Creator
				</h2>
				<p>
Make your keyguide you desire here! Please note that this is very very early beta. Lots of things aren't working! If you are interested in playing around with this more take a look at <a href="https://github.com/willwade/KeyGuideMaker">the github project page</a> which provides a line command tool to make your own keyguide. <br /><br />If you want to try creating just a basic grid of cells for laser cutting try using <a href="gridtemplater.html">the GridTemplater tool</a>. <br /><br />Credit for these tools go to
<a href="https://twitter.com/si_judge">Simon</a>, <a href="http://christopherjbarr.weebly.com/">Chris</a> and <a href="https://twitter.com/willwade">Will</a> and its all under a <a href="https://github.com/willwade/KeyGuideMaker#licence">CC-A licence</a>				</p>
			</div>
			<ul>
				<li id="li_1">
					<label class="description" for="element_1">
						Choose your device (& options if any)
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
					<label class="description" for="element_file">
						<input type="checkbox" data-related-item="element_file" name="usefile" id="usefile" value="1"/> Upload a template element to overlay? 
					</label>
					<div class="hidden">
						<input id="element_file" name="file" class="element file" type="file"/> <br />
						x: <input type="text" size="5"  maxlength="5" name="xpos" id="xpos" value="60"/>  y: <input type="text" size="5" name="ypos" id="ypos" maxlength="5" value="90"/><br />(from top left. NB: enter Nmm otherwise assumes pixels) 
					</div>
					<p class="guidelines" id="guide_1">
						<small>
							Upload a SVG file to overlay in the window of the device. Note takes the window dimensions of the device template and places it in the correct place. 
						</small>
					</p>
				</li>
				<li id="li_4">
					<label class="description" for="element_4">
						What type of laser cutting machine is this for? 
					</label>
					<select class="element select medium" id="formachine" name="formachine">
							<option value="epilog-mini" selected="selected">
								Epilog Mini (Black, 0.01mm lines)
							</option>
							<option value="ponoko">
                                Ponoko / Razorlab (Blue, 0.01mm lines)
							</option>
						</select>
				<p class="guidelines" id="guide_4"><small>Some laser cutting machines need blue lines, some black for cutting lines. Choose the colour of the lines here</small></p></li>

				<li id="li_5">
					<label class="description" for="element_5">
						Choose the final format
					</label>
					<select class="element select medium" id="format" name="format">
							<option value="svg" selected="selected">
                                SVG
							</option>
							<option value="wmf">
								WMF
							</option>
							<option value="eps">
								EPS
							</option>
							<option value="pdf">
								PDF
							</option>
						</select>
				<p class="guidelines" id="guide_5"><small>SVG recommended - the conversion isn't very good</small></p></li>

				<li class="section_break">
			<h3>Tips!</h3>
			<p>Once downloaded you need to send this to your <a href="http://lmgtfy.com/?q=laser+cutting">local laser cutting service</a>, <a href="http://www.fablabmanchester.org/about-us/fab-lab-network">fablab</a>,your helpful AT company of choice (<a href="http://www.smartboxat.com">Smartbox</a>, <a href="http://www.logan-technologies.co.uk">Logan</a> for example) or, if you want to use card, just print and cut!. Note that guides work best between 2mm and 3mm thickness. 6mm is quite chunky and can be tricky with small cell apps. You may need to purchase some acrylic (for example <a href="http://www.directplasticsonline.co.uk/">these folks</a> sell it pretty cheaply in the UK). Card, leather and all sorts of other materials can be used. We only ask you <a href="javascript:void(0)" data-uv-lightbox="classic_widget" data-uv-mode="full" data-uv-primary-color="#cc6d00" data-uv-link-color="#007dbf" data-uv-default-mode="support" data-uv-forum-id="215520">feedback</a> your results to us so we can improve the designs!</p>
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

<!-- UserVoice JavaScript SDK (only needed once on a page) -->
<script>(function(){var uv=document.createElement('script');uv.type='text/javascript';uv.async=true;uv.src='//widget.uservoice.com/jIbNm5WiTQTNqulGMGWyJQ.js';var s=document.getElementsByTagName('script')[0];s.parentNode.insertBefore(uv,s)})()</script>
<!-- A tab to launch the Classic Widget -->
<script>
UserVoice = window.UserVoice || [];
UserVoice.push(['showTab', 'classic_widget', {
  mode: 'full',
  primary_color: '#cc6d00',
  link_color: '#007dbf',
  default_mode: 'support',
  forum_id: 215520,
  tab_label: 'Feedback & Support',
  tab_color: '#cc6d00',
  tab_position: 'middle-right',
  tab_inverted: false
}]);
</script>
</body>
</html>
