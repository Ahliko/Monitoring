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
chown -R monit:monit /var/monit
chown -R monit:monit /usr/local/lib64/monit
chown -R monit:monit /var/log/monit.log
chown -R monit:monit /usr/local/bin/server.sh

# Change permission

chmod 755 /usr/local/bin/server.sh

# Reload daemon
systemctl daemon-reload

# Open firewall
firewall-cmd --permanent --add-port=50051/tcp
firewall-cmd --reload

# Enable monit service
if [ "$(systemctl is-enabled monit.service)" -eq 0 ]; then
    systemctl enable monit.service
fi

# Start monit service
if [ "$(systemctl is-active monit.service)" -eq 0 ]; then
    systemctl restart monit.service
else
    systemctl start monit.service
fi


# Check status
systemctl status monit.service
