import os

if not os.path.exists('/var/log/monit.log'):
    os.system('touch /var/log/monit.log')
    os.system('chown $USER:$USER /var/log/monit.log')

if not os.path.exists('/var/monit'):
    os.system('mkdir /var/monit')
    os.system('chown $USER:$USER /var/monit')

if not os.path.exists('/etc/monit'):
    os.system('touch /etc/monit')
    os.system('chown $USER:$USER /etc/monit')

if not os.path.exists('/etc/monit/monit.json'):
    os.system('touch /etc/monit/monit.json')
    os.system('chown $USER:$USER /etc/monit/monit.json')
