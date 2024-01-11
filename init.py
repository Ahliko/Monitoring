import os
import pwd

try:
    pwd.getpwnam('monit')
except KeyError:
    os.system('useradd monit --shell /sbin/nologin')

if not os.path.exists('/var/monit'):
    os.system('mkdir /var/monit')
    os.system('chown monit:monit /var/monit')

if not os.path.exists('/var/log/monit.log'):
    os.system('touch /var/log/monit.log')
    os.system('chown monit:monit /var/log/monit.log')

if not os.path.exists('/etc/monit'):
    os.system('mkdir /etc/monit')
    os.system('chown monit:monit /etc/monit')

if not os.path.exists('/etc/monit/monit.json'):
    os.system('touch /etc/monit/monit.json')
    os.system('chown monit:monit /etc/monit/monit.json')

os.system('cp monit.py /usr/bin/monit.py')
os.system('chmod +x /usr/bin/monit.py')
os.system('pip install psutil')
os.system('pip install colorlog')