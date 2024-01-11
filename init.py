import os
import pwd

if pwd.getpwnam('monit') is None:
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
