<html>

<head>
<title>Send CAN Message</title>
</head>

<body>


<form action="send.php" method="post">
ID:  <input type="text" name="msg_id" value="400" size ="4" />

Data:  <input type="text" name="msg_data" size="20" />

<input type="submit" name="submit" value="Submit" />
</form>

<i>NB: Cansend accepts numbers ina hexadecimal format with the first byte to the left. </i>

<?php

if(isset($_POST['submitted'])) {
  echo( "thanks blud." );
}

?>

</body>
</html>
