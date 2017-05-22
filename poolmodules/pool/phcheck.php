<?php
header("Refresh: 300; url=phcheck.php");

include "/var/www/db.php";

$datum = date("d.m.Y");
$uhrzeit = date("H:i");

$sql = "SELECT Datum, Uhrzeit, Wert, Counter, PHminus
        FROM sensorchecks WHERE Sensor='PH'"; 
$result = mysql_query($sql) OR die(mysql_error()); 
echo $result;
$row = mysql_fetch_assoc($result);  

$date = new datetime($row['Datum']);
$time = new datetime($row['Uhrzeit']);

$ini_array = array("Datum"=>$date->format('d.m.Y'), "Uhrzeit"=>$time->format('H:i'), "PH"=>$row['Wert'], "Counter"=>$row['Counter'], "PHminus"=>$row['PHminus']);
print_r($ini_array);
/*   echo "<br>";   */

if (strtotime($ini_array["Datum"]) <> strtotime(date("d.m.Y"))) {
	$ini_array['PHminus'] = 0;
}

$sql = "SELECT timestamp, ph 
        FROM ph WHERE sensor_id=3
        ORDER BY timestamp DESC LIMIT 0,1;"; 
$result = mysql_query($sql) OR die(mysql_error()); 
$row = mysql_fetch_assoc($result);  

$date = new DateTime($row['timestamp']);
$sql_array = array("Datum"=>$date->format('d.m.Y'), "Uhrzeit"=>$date->format('H:i'), "PH"=>$row['ph']);
print_r($sql_array);
/*   echo "<br>";   */

include "/var/www/actions/gpio_values.php";
if ($gpio31 == 1) {
	/*   echo "Pumpe aus!";   */
	} else {
	$ini_time = strtotime($ini_array["Datum"]." ".$ini_array["Uhrzeit"]);
	$sql_time = strtotime($sql_array["Datum"]." ".$sql_array["Uhrzeit"]);
	$timediff = ($sql_time - $ini_time) / 60;

	switch (true) {
		case (((strtotime($Datum." ".$Uhrzeit) - $sql_time) / 60) > 8):
			/*   echo "SQL Daten zu alt!";   */
			$ini_array['Counter'] = 0;
			/* PH: Messung gesartet ins LOG */
			$logentry = "PH: Messung gesartet";
			$sql = "INSERT INTO log (entry, value) VALUES ('".$logentry."', '".$ini_array['PH']."');"; 
			$result = mysql_query($sql) OR die(mysql_error()); 
			break;
		case ($timediff > 8):
			/*   echo "timediff_".$ini_array['Counter']++;   */
			/*schreibe neue ini (Counter = 1)*/
			$ini_array['Datum'] = $sql_array['Datum'];;
			$ini_array['Uhrzeit'] = $sql_array['Uhrzeit'];;
			$ini_array['PH'] = $sql_array['PH'];;
			$ini_array['Counter'] = 1;
			/* PH: Messung gesartet ins LOG */
			$logentry = "PH: Messung gesartet";
			$sql = "INSERT INTO log (entry, value) VALUES ('".$logentry."', '".$ini_array['PH']."');"; 
			$result = mysql_query($sql) OR die(mysql_error()); 
			break;
		case ($ini_array['Counter'] == 0):
			$ini_array['Datum'] = $sql_array['Datum'];;
			$ini_array['Uhrzeit'] = $sql_array['Uhrzeit'];;
			$ini_array['PH'] = $sql_array['PH'];;
			$ini_array['Counter'] = 1;
			break;

		case ($ini_array['Counter'] == 5):
			/*   echo "Counter_".$ini_array['Counter']++.", ";   */
			if ($sql_array['PH'] < $ini_array['PH']) {
				$ini_array['PH'] = $sql_array['PH'];
				}
			/*PH Kontrolle und ggf. Korrektur*/

			switch (true) {
			    case ($ini_array["PH"] > 8.5):
			        /*   echo "da mach i nix (>8,5)";   */
				$logentry = "PH: PH-Wert zu hoch, keine definierte Aktion. PH manuell prüfen!";
			        break;
			    case ($ini_array["PH"] < 6.5):
			        /*   echo "da mach i nix (<6,5)";   */
				$logentry = "PH: PH-Wert zu niedrig, keine definierte Aktion. PH manuell prüfen!";
			        break;
			    case ($ini_array["PH"] > 7.35):

				if ($ini_array['PHminus'] >= 5) {
					$logentry = "PH: PH Minus Tageshöchstwert erreicht! Keine Aktion.";
				} else {
					shell_exec('run_phm_1min.sh');
					$logentry = "PH: PH Minus eingespült";
					$ini_array['PHminus']++;
				}

			        /*   echo "Da sollte PH Minus rein<br>".$logentry;   */
			        break;
			    case ($ini_array["PH"] < 7.15):
			        /*   echo "da sollte PH Plus rein";   */
				$logentry = "PH: PH Plus nicht vorhanden, keine Aktion";
			        break;
			    default:
				/*   echo "alles bestens";   */
				$logentry = "PH: Keine Aktion nötig";
				break;
			}
	
			/*schreibe neue ini (Counter = 0)*/
			$ini_array['Datum'] = $sql_array['Datum'];;
			$ini_array['Uhrzeit'] = $sql_array['Uhrzeit'];;
			$ini_array['Counter'] = 0;
			/*schreibe LOG*/
			$sql = "INSERT INTO log (entry, value) VALUES ('".$logentry."', '".$ini_array['PH']."');"; 
			$result = mysql_query($sql) OR die(mysql_error()); 

			break;
		default:
			if ($sql_array['PH'] < $ini_array['PH']) {
				$ini_array['PH'] = $sql_array['PH'];
				}
			/*schreibe neue ini (Counter = addiert)*/
			/*   echo "default_".$ini_array['Counter']++;   */
			$ini_array['Datum'] = $sql_array['Datum'];;
			$ini_array['Uhrzeit'] = $sql_array['Uhrzeit'];;
			$ini_array['Counter'] = $ini_array['Counter']++;
			break;
	
	}
	/*   echo "<br>";
	echo "<br>";   */
	$date = new DateTime($ini_array["Datum"]);

	$db_array = array("Datum"=>$date->format('Y-m-d'), "Uhrzeit"=>$ini_array["Uhrzeit"], "Wert"=>$ini_array["PH"], "Counter"=>$ini_array["Counter"], "PHminus"=>$ini_array["PHminus"]);
	print_r($db_array);
	/*   echo "<br>";   */

	$stmt= $db_array;
	$query= 'UPDATE sensorchecks SET ';
	foreach( $stmt AS $k => $v ) {
	  $query.= $k.'="'.$v; 
	  if ( $k !== "PHminus") $query.= '", ';
	  if ( $k == "PHminus") $query.= '" WHERE (((Sensor)="PH"));';
	}
	/*   echo $query;   */
	$result = mysql_query($query) OR die(mysql_error()); 



}


?>