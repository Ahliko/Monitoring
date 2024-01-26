"""
Install monit
"""
import os
import pwd

try:
    pwd.getpwnam('monit')
except KeyError:
    os.system('useradd monit --shell /sbin/nologin')

if not os.path.exists('/var/monit'):
    os.system('mkdir /var/monit')
    os.system('chown monit:monit /var/monit')

if not os.path.exists('/var/monit/monit_conf.json'):
    os.system('touch /var/monit/monit_conf.json')
    os.system('chown monit:monit /var/monit/monit_conf.json')
    os.system('echo {"CHECK_PORTS": []} > /var/monit/monit_conf.json')

if not os.path.exists('/var/log/monit.log'):
    os.system('touch /var/log/monit.log')
    os.system('chown monit:monit /var/log/monit.log')

if not os.path.exists('/etc/monit'):
    os.system('mkdir /etc/monit')
    os.system('chown monit:monit /etc/monit')

if not os.path.exists('/etc/monit/monit.json'):
    os.system('touch /etc/monit/monit.json')
    os.system('chown monit:monit /etc/monit/monit.json')

os.system('cp monit.py /usr/local/bin/server.py')
os.system('chmod +x /usr/bin/monit.py')

if os.system('pip --version 2> /dev/null') != 0:
    os.system('dnf install python3-pip -y')

os.system('pip install psutil')
os.system('pip install colorlog')
os.system('pip install fire')
