<html>

<head>
<title>Send CAN Message</title>
</head>

<body>


<form action="send.php" method="post">
<input type="hidden" name="submitted" value="TRUE" />
  
ID:  <input type="text" name="msg_id" value="400" size ="4" />

Data:  <input type="text" name="msg_data" size="20" />

<input type="submit" name="submit" value="Submit" />
<input type="reset" name="reset" value="Reset" />
</form>

<i>NB: Cansend accepts numbers ina hexadecimal format with the first byte to the left. </i>

<br><br>

<?php

if(isset($_POST['submitted'])) {
  
  $msg_id = trim($_POST['msg_id']);
  $msg_data = trim9$_POST['msg_data']);
  
  if (!ctype_xdigit($msg_id)) echo( "nah fam, " . $msg_id . " aint a hex string, you get me?" );
  if (!ctype_xdigit($msg_data)) echo( "nah fam, " . $msg_id . " aint a hex string, you get me?" );
  $msg = '' . $msg_id . "#" . $msg_data;
  echo( "thanks blud, u just sent a message wot be " . $msg );
  
  
}

?>

</body>
</html>
