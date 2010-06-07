<?php 
include("arecibo.php");
$fields = array(
    "account" => "432dfb1c43bca8231ed5a5ae5e904132",
);
post("http://areciboapp.appspot.com/v/1/", $fields)
?>