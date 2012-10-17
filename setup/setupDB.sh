sudo yum list installed | grep "postgres" | gawk '{ print $1 }' | sudo xargs yum remove -y
sudo yum install /usr/include/libpq-fe.h -y
sudo yum install postgresql -y
sudo yum install postgresql-server -y
sudo rm -rf /var/lib/pgsql/data
sudo postgresql-setup initdb
sudo systemctl enable postgresql.service
sudo systemctl start postgresql.service
echo "begin user creation, please word password: 403-kamal"
sudo su -c "createuser --superuser -P pgadmin" postgres
sudo su -c "createdb --encoding=utf-8 --owner=pgadmin instafeed" postgres
sudo sed -ri s/"(peer|ident)"$/md5/ /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql.service
psql -U pgadmin instafeed < database/dump.txt
