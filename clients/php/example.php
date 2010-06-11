<?php 
include("arecibo.php");
$fields = array(
    "account" => "w3;5qwy45qshtqu46tdtgheq47s.ert6ew45e4i2w65",
);
post("http://test-areciboapp.appspot.com/v/1/", $fields)
?>