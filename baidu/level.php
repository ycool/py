;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

<?php

$soapClient = new soapClient('http://noah.baidu.com/noah/index.php?r=userPermitService/ws');

$userName = $argv[1];
var_dump($userName);
$user = $soapClient->getNoahUserByName($userName);
//$user = $soapClient->getNoahUserById($userName);

var_dump($user);

?>
