#!/usr/bin/env sh

gzip -d GPMal.tar.gz
tar -xvf -C /opt/ GPMal.tar
cd /opt/gpmall/
tar -xvf gpmall.tar
touch /etc/yum.repos.d/resis.repo
echo "[Redis]" >> /etc/yum.repos.d/resis.repo
echo "name=redis" >> /etc/yum.repos.d/resis.repo
echo "baseurl=file:///opt/gpmall/gpmall/" >> /etc/yum.repos.d/resis.repo
echo "enabled=1" >> /etc/yum.repos.d/resis.repo
echo "gpgcheck" >> /etc/yum.repos.d/resis.repo

yum repolist
yum install -y redis

sed -i 's/bind 127.0.0.1/bind 0.0.0.0/'g /etc/redis.conf
sed -i 's/protected-mode no/protected-mode yes/'g /etc/redis.conf

/usr/bin/redis-server &