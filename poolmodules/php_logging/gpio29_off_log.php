<?php
mysql_connect("localhost","root","ibo43har") or die ("Keine Verbindung moeglich");
mysql_select_db("pool") or die ("Die Datenbank existiert nicht.");

$sql = "INSERT INTO log (entry) VALUES ('Socket-1: PHminus (run_phm_1min.sh): Power Off');"; 
			$result = mysql_query($sql) OR die(mysql_error()); 
?>