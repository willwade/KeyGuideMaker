#KeyGuideMaker - Web Front end#

A quick overview of the files here:

* index.html. A simple HTML form created by [phpform](http://www.phpform.org/formbuilder/view.php?id=min7hopgn0rhucrl413lt5mbr0). It contains some jquery to populate the dropdowns. Note that index is static - its not php but is created by "createindex.php" on a cron job (or when the types and keyguide options have been updated). Note index calls:
* ajax_templates.php. Simply populates the dropdowns from the db/Types.. csv files
* guidecreator.php. The php script that gets called when a index form is posted. Its pretty rough and ready in places. Watch your step.

Note there is currently a lot of hard coding of "Types"  being 1,2,3 etc..
