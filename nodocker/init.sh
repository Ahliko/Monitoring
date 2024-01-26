#!/usr/bin/env bash

# Install dependencies
pip install -r requirements.txt

# create user monit
useradd -m monit -s /sbin/nologin

# Create folders
mkdir -p /var/monit

# Create log file
touch /var/log/monit.log

# Copy files
cp -r monit /usr/local/lib64/
cp server.sh /usr/local/bin

# Copy monit.service
cp monit.service /etc/systemd/system/monit.service

# change owner
chown -R monit:monit /var/monit \
  /usr/local/lib64/monit \
  /var/log/monit.log \
  /usr/local/bin/server.sh

# Change permission

chmod 755 /usr/local/bin/server.sh

# Reload daemon
systemctl daemon-reload

# Open firewall
firewall-cmd --add-port=50051/tcp
firewall-cmd --runtime-to-permanent
