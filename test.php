<html>
<head>
<!--
 <meta http-equiv="refresh" content="5"> 
-->
<title>Welcome to nginx!</title>
</head>

<body bgcolor="white" text="black">
<center><h1>Hello World</h1></center>

<?php

function hexTo32Float($strHex) {
    $v = hexdec($strHex);
    $x = ($v & ((1 << 23) - 1)) + (1 << 23) * ($v >> 31 | 1);
    $exp = ($v >> 23 & 0xFF) - 127;
    return $x * pow(2, $exp - 23);
}

// Connect to MySQL
$dbc = @mysql_connect( 'localhost', 'root', 'dusc2015' )
	OR die ( 'Could not connect to MySQL: ' . mysql_error() );

//Select database
@mysql_select_db( 'test' ) OR die ( 'Could not select database: ' .  mysql_error( ) );


$result = mysql_query ( 'SELECT * FROM can WHERE msg_id = 1281 LIMIT 1;' );

while ( $row = mysql_fetch_array( $result, MYSQL_ASSOC ) ) {
        echo('Speed: ');
        echo(hexTo32Float(bin2hex( substr($row['msg_data'], 4, 4) )) . '<br>' );
}

echo('<br><br><br>');

//Print out last recieved messages
// SELECT * FROM can WHERE msg_id BETWEEN 0 AND 1000 ORDER BY msg_id ASC LIMIT 5;
$result = mysql_query ( 'SELECT * FROM can LIMIT 10;' );
while ( $row = mysql_fetch_array( $result, MYSQL_ASSOC ) ) {
	echo($row['msg_no'] . ', ' . $row['msg_id'] . ', ');
	echo('0x' .  bin2hex($row['msg_data']) . '<br>' );
}

?>


</body>
</html>
