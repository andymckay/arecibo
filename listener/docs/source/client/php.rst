Sample PHP Client
====================================

The PHP client allows you to easily send errors via HTTP. The PHP client can be used independently, or as part of a greater implementation. Quick example:

<?php
include("arecibo.php");
$fields = array(
    "account" => "yourpublicaccountnumber",
    "status" => "403",
    "url" => "http://badphpapp.org"
);
post($fields);
?>

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Tested on PHP 5.2.6. 

* If using the http client, permission to make a HTTP post to the Arecibo server is needed.

Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~

* No values are automatically set.