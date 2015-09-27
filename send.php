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
<!--<input type="reset" name="reset" value="Reset" /> -->
<input type="submit" name="reload" value="Reload" />
</form>

<i>NB: Cansend accepts numbers ina hexadecimal format with the first byte to the left. </i>

<br><br>

<?php

if(isset($_POST['submit'])) {
  
  $msg_id = str_pad( trim($_POST['msg_id']), 3, "0", STR_PAD_LEFT);
  $msg_data = trim($_POST['msg_data']);
  
  if (!ctype_xdigit($msg_id)) {
    echo( "nah fam, " . $msg_id . " aint a hex string, you get me?" );
  } else if (($msg_data != '') && !ctype_xdigit($msg_data)) {
    echo( "nah fam, " . $msg_data . " aint a hex string, you get me?" );
  } else {
    $msg = '' . $msg_id . "#" . $msg_data;
    //N>B: This is potentially a massive security flaw.
    echo( "thanks blud, u just sent a message wot be " . $msg . ", boomshanka. Errors here: ");
    echo( shell_exec("cansend can0 $msg 2>&1") );
  }
  
}

?>

</body>
</html>
