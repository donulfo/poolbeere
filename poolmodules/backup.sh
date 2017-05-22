#/bin/bash

mkdir /tmp/backup

/etc/webmin/mysql/backup.pl --all

### ausgelagert in webmin (sql backup)
#service mysql stop
#rsync -a /var/lib/mysql/pool /usr/local/sbin/_mysql_backup/
#rsync -a /var/lib/mysql/garten /usr/local/sbin/_mysql_backup/
#tar czf /tmp/backup/pool_sql.tar.gz /var/lib/mysql/pool
#tar czf /tmp/backup/garten_sql.tar.gz /var/lib/mysql/garten
#service mysql start

du -sh /var/lib/mysql/pool > /tmp/backup/du-sh_mysql_pool.txt
du -sh /var/lib/mysql/garten > /tmp/backup/du-sh_mysql_garten.txt

service apache2 stop

tar --exclude="/usr/local/sbin/_*" -czf /tmp/backup/usr_local_sbin.tar.gz /usr/local/sbin
tar czf /tmp/backup/var_www.tar.gz /var/www

service apache2 start

cp /var/spool/cron/crontabs/root /tmp/backup/cron_root.txt
df -h > /tmp/backup/df-h.txt

#apt-get install ncftp
ncftpput -R -u "mschraml" -p "Diabolo%17" 192.168.99.99 /Backups/PoolPi /tmp/backup
ncftpput -u "mschraml" -p "Diabolo%17" 192.168.99.99 /Backups/PoolPi /usr/local/sbin/*.sh

rm -r /tmp/backup*

