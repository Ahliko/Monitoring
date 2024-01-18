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
        self.__logger = self.__get_logger()
        self.__path = "/var/monit"

    @staticmethod
    def __get_logger() -> logging.Logger:
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
                self.__logger.info(f)

    def __check_cpu(self):
        cpu_percent = psutil.cpu_percent()
        self.__logger.info(f"CPU usage: {cpu_percent}%")
        return cpu_percent

    def __check_ram(self):
        ram_percent = psutil.virtual_memory().percent
        self.__logger.info(f"RAM usage: {ram_percent}%")
        return ram_percent

    def __check_disk(self):
        disk_percent = psutil.disk_usage("/").percent
        self.__logger.info(f"Disk usage: {disk_percent}%")
        return disk_percent

    def __check_port(self):
        if not os.path.exists(f'{self.__path}/monit_conf.json'):
            os.system(f'touch {self.__path}/monit_conf.json')
        with open(f"{self.__path}/monit_conf.json", "r") as f:
            try:
                data = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                data = {"CHECK_PORTS": []}
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return [sock.connect_ex(("127.0.0.1", port)) == 0 for port in data["CHECK_PORTS"]]

    def check(self):
        with open(f"{self.__path}/check_{datetime.datetime.now()}.json", "a") as f:
            self.__logger.info(f"Ecriture dans : {self.__path}/check_{datetime.datetime.now()}.json")
            f.write(f"Date : {datetime.datetime.now()}\n")
            f.write(f"ID : {uuid.uuid4()}\n")
            f.write(f"CPU : {self.__check_cpu()}\n")
            f.write(f"RAM : {self.__check_ram()}\n")
            f.write(f"Disk : {self.__check_disk()}\n")
            f.write(f"Port : {self.__check_port()}\n")

    def last(self):
        last_file = max(glob.glob(self.__path + "*"), key=os.path.getctime)
        self.__logger.info(f"Last file: {last_file}")
        print(last_file)

    def __last_x_hour_file(self, hours: int):
        hours *= 3600
        file_list = []
        for file in os.listdir(self.__path):
            if file.startswith("check_") and os.path.getmtime(self.__path + file) > time.time() - hours:
                file_list.append(self.__path + file)
        self.__logger.info(f"Files from last {hours / 3600} hours: {file_list}")
        return file_list

    def avg(self, hours: int):
        file_list = self.__last_x_hour_file(hours)
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
        self.__logger.info(f"Average CPU usage: {cpu_avg}%")
        self.__logger.info(f"Average RAM usage: {mem_avg}%")
        self.__logger.info(f"Average Disk usage: {disk_avg}%")
        print("cpu: %.2f\nmem: %.2f\ndisk: %.2f" % (cpu_avg, mem_avg, disk_avg))



if __name__ == '__main__':
    fire.Fire(Monitoring)
