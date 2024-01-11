#! /usr/bin/env python3
import datetime
import socket

import psutil
import time
import os
import colorlog
import logging
import argparse
import json

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/var/log/monit.log', 'w', 'utf-8')
file_handler.setLevel(logging.INFO)
stream_handler = colorlog.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

argparser = argparse.ArgumentParser()
argparser.add_argument('check', help='Run a check test')
argparser.add_argument('list', help='Return the list of all check')
argparser.add_argument('get', help='Get last check or a data avg of X last hour', choices=['last', 'avg'])


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_mem_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage('/').percent


def get_tcp_port_open(lst):
    res = []
    for port in lst:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', port))
            s.close()
            res.append(True)
        except Exception as e:
            res.append(False)
    return res if res else None


def get_conf_tcp_ports():
    if not os.path.exists('/etc/monit/monit.json'):
        logger.warning('No monit.conf found')
        return []
    else:
        logger.info('Found monit.conf')
        with open('/etc/monit/monit.json', 'r') as f:
            try:
                data = json.load(f)
                return data['tcp_ports']
            except Exception as e:
                logger.error('Error while loading monit.conf: {}'.format(e))
                return []


def write_rapport(rapport):
    if not os.path.exists('/var/monit'):
        logger.error('No monit folder found')
        exit(1)
    with open(f'/var/monit/rapport_{datetime.date.today()}.json', 'w') as f:
        try:
            json.dump(rapport, f)
        except Exception as e:
            logger.error('Error while writing rapport: {}'.format(e))


def check():
    logger.info('Starting check')
    rapport = {'cpu': get_cpu_usage(), 'mem': get_mem_usage(), 'disk': get_disk_usage(),
               'tcp': get_tcp_port_open(get_conf_tcp_ports())}
    write_rapport(rapport)
    logger.info('Ending check')


def get_list():
    if not os.path.exists('/var/monit'):
        logger.error('No monit folder found')
        exit(1)
    files = os.listdir('/var/monit')
    files.sort()
    for file in files:
        if file.startswith('rapport_'):
            print(file)


def get_last():
    if not os.path.exists('/var/monit'):
        logger.error('No monit folder found')
        exit(1)
    files = os.listdir('/var/monit')
    files.sort()
    file = files[-1]
    if file.startswith('rapport_'):
        with open(f'/var/monit/{file}', 'r') as f:
            try:
                data = json.load(f)
                print(f'File: {file}')
                print(f'CPU: {data["cpu"]}')
                print(f'MEM: {data["mem"]}')
                print(f'DISK: {data["disk"]}')
                print(f'TCP: {data["tcp"]}')
            except Exception as e:
                logger.error('Error while loading rapport: {}'.format(e))
                return []


def get_x_last_hour_avg(args):
    if not os.path.exists('/var/monit'):
        logger.error('No monit folder found')
        exit(1)
    files = os.listdir('/var/monit')
    files.sort()
    nowhour = datetime.datetime.today().hour
    nowdate = datetime.datetime.today().day
    if args % 24 - nowhour < 0:
        hit_hours = args % 24 - nowhour + 24
        hit_days = args // 24 - 1
    else:
        hit_hours = args % 24 - nowhour
        hit_days = args // 24
    hit_files = []


def main():
    args = argparser.parse_args()
    if args.check == 'check':
        check()
    elif args.check == 'list':
        get_list()
    elif args.check == 'get':
        if args.get == 'last':
            get_last()
        elif args.get == 'avg':
            get_x_last_hour_avg(argparser.parse_args())

    else:
        print('No check found')


if __name__ == '__main__':
    main()
