#! /usr/bin/env python3
import datetime
import logging

import colorlog
import psutil
import socket
import json
import uuid
import os
import glob
import time
import fire


class Monitoring:
    def __init__(self):
        self.__logger = self.get_logger()
        self.__path = "/var/monit"

    @staticmethod
    def get_logger() -> logging.Logger:
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
        return logger

    def list(self):
        for f in os.listdir(self.__path):
            if f.startswith("check_"):
                print(f)

    @staticmethod
    def check_cpu():
        return psutil.cpu_percent()

    @staticmethod
    def check_ram():
        return psutil.virtual_memory().percent

    @staticmethod
    def check_disk():
        return psutil.disk_usage("/").percent

    @staticmethod
    def check_port():
        with open("monit_conf.json", "r") as f:
            data = json.load(f)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in data["CHECK_PORTS"]:
            return sock.connect_ex(("127.0.0.1", port)) == 0

    def check(self):
        with open(f"{self.__path}/check_{datetime.datetime.now()}.json", "a") as f:
            f.write(f"Date : {datetime.datetime.now()}\n")
            f.write(f"ID : {uuid.uuid4()}\n")
            f.write(f"CPU : {self.check_cpu()}\n")
            f.write(f"RAM : {self.check_ram()}\n")
            f.write(f"Disk : {self.check_disk()}\n")
            f.write(f"Port : {self.check_port()}\n")

    def last(self):
        print(max(glob.glob(self.__path + "*"), key=os.path.getctime))

    def last_x_hour_file(self, hours: int):
        hours *= 3600
        file_list = []
        for file in os.listdir(self.__path):
            if file.startswith("check_") and os.path.getmtime(self.__path + file) > time.time() - hours:
                file_list.append(self.__path + file)
        return file_list

    def avg(self, hours: int):
        file_list = self.last_x_hour_file(hours)
        cpu = []
        mem = []
        disk = []
        for file in file_list:
            with open(file, "r") as f:
                for line in f:
                    if line.startswith("cpu"):
                        cpu.append(float(line.split(":")[1].strip()))
                    elif line.startswith("mem"):
                        mem.append(float(line.split(":")[1].strip()))
                    elif line.startswith("disk"):
                        disk.append(float(line.split(":")[1].strip()))
        cpu_avg = sum(cpu) / len(cpu)
        mem_avg = sum(mem) / len(mem)
        disk_avg = sum(disk) / len(disk)
        print("cpu: %.2f\nmem: %.2f\ndisk: %.2f" % (cpu_avg, mem_avg, disk_avg))

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value
