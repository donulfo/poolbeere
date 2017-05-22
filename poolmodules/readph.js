function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

var MiniPh = require('./index.js');

var miniPh = new MiniPh('/dev/i2c-1', 0x4e);

var _mysql = require('./node_modules/mysql');

var Zaehler = 1;
var PHwert = 0;

var HOST = 'localhost';
var PORT = 3306;
var MYSQL_USER = 'root';
var MYSQL_PASS = 'ibo43har';
var DATABASE = 'pool';
var TABLE = 'ph';

var mysql = _mysql.createConnection({
    host: HOST,
    port: PORT,
    user: MYSQL_USER,
    password: MYSQL_PASS,
});

mysql.query('use ' + DATABASE);


//console.log(MiniPh.params);
miniPh.calcpHSlope();
//console.log(MiniPh.params);
//miniPh.saveConfig();


while (Zaehler <= 450) {

	miniPh.readPh(function (err, m) {
		sleep(100);
		if (err) {
			console.log(err);
		} else {
//			console.log({
//				raw : m.raw,
//				pH : m.ph,
//				filter: m.filter
//			});
      if (Zaehler > 350) {
			 PHwert = PHwert + m.ph;
      }
		}
	});


	Zaehler++;
}

PHwert = Math.round((PHwert/100)*100)/100;
console.log(Zaehler);
console.log(PHwert);

//console.log("- RUN SQL Statement:")
//console.log("    select id from sensors where hardware_id = '0x4e'");

if (PHwert > 6.4 && PHwert < 8.4) {
console.log("Schreibe in die Datenbank")

mysql.query('select id from sensors where hardware_id = "0x4e"', function(err, result, fields) {
    if (err) {console.log(err)}
    else {
            var row = result[0];
		//console.log(row.id);

		//console.log("- RUN SQL Statement:")
		//console.log("    insert into '+ TABLE +' (sensor_id,raw,ph,filter)");

//		mysql.query('insert into '+ TABLE +' (sensor_id,raw,ph,filter) values (' + row.id + ',"' + m.raw + '","' + m.ph + '","' + m.filter + '")',
		mysql.query('insert into '+ TABLE +' (sensor_id,raw,ph,filter) values (' + row.id + ',"' + m.raw + '","' + PHwert + '","' + m.filter + '")',
		
		function selectCb(err, results, fields) {
		    if (err) throw err;
		    else console.log('success');
		});

    }
});

}
else {
console.log("Vermutliche Fehlmessung, verwerfe PH-Wert")
}



//nur quatsch zum beenden des scripts
mysql.query('select quatsch from quatsch where quatsch = "quatsch"', function(err, result, fields) {
    if (err) {null.dummy}
    else {null.dummy

    }
});


