<html>
<head>
<?php
	 //echo('<meta http-equiv="refresh" content="3">';
?> 
<!-- -->
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


$result = mysql_query ( 'SELECT * FROM can WHERE msg_id = 1281 ORDER BY msg_no DESC LIMIT 1;' );

while ( $row = mysql_fetch_array( $result, MYSQL_ASSOC ) ) {
        echo('Speed: ');
	//$data = pack('f2', 30.87, 60.56);
        $data = $row['msg_data'];
	//echo( hexTo32Float(bin2hex( substr( $data, 4, 4) )) . '<br>' );
	$floats = unpack('f2', $data);
	echo( $floats['1'] . ', Current: ' . $floats['2'] );

	/* $afloat = 46;
	$afloatdata = pack("f", $afloat);
	echo( bin2hex( $afloatdata ) . ", " );
	$afloatarray = unpack("H4a/H4b", $afloatdata);
	echo( $afloatarray['b'] ); */
}

echo('<br><br><br>');

//Print out last recieved messages
// SELECT * FROM can WHERE msg_id BETWEEN 0 AND 1000 ORDER BY msg_id ASC LIMIT 5;
$result = mysql_query ( 'SELECT * FROM can ORDER BY msg_no DESC LIMIT 10;' );
while ( $row = mysql_fetch_array( $result, MYSQL_ASSOC ) ) {
	echo($row['msg_no'] . ', ' . $row['msg_id'] . ', ');
	echo('0x' . strrev( unpack('h*hex', $row['msg_data'])['hex'] ) . '<br>' );
}

?>


</body>
</html>
