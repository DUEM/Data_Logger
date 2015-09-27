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
  
  $msg_id = $_POST['msg_id'];
  $msg_data = $_POST['msg_data'];
  $msg = '' . $msg_id . "#" . $msg_data
  echo( "thanks blud, u just sent a message wot be " . $msg );
  
  
}

?>

</body>
</html>
