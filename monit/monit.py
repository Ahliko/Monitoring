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
import json


class Monitoring:
    def __init__(self):
        self.__logger = self.__get_logger()
        self.__path = "/var/monit/"

    @staticmethod
    def __get_logger() -> logging.Logger:
        logger = colorlog.getLogger()
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('/var/log/monit.log', 'w', 'utf-8')
        file_handler.setLevel(logging.DEBUG)
        stream_handler = colorlog.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

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
        lst = []
        for f in os.listdir(self.__path):
            if f.startswith("check_"):
                self.__logger.info(f)
                lst.append(f)
        return lst

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
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        myjson = {
            "Date": date,
            "ID": str(uuid.uuid4()),
            "CPU": self.__check_cpu(),
            "RAM": self.__check_ram(),
            "Disk": self.__check_disk(),
            "Port": self.__check_port()
        }
        with open(f"{self.__path}check_{date}.json", "a") as f:
            self.__logger.info(f"Ecriture dans : {self.__path}check_{date}.json")
            f.write(json.dumps(myjson))

    def __last(self):
        last_file = max([self.__path + f for f in os.listdir(self.__path) if f.startswith("check_")],
                        key=os.path.getctime)
        self.__logger.info(f"Last file: {last_file}")
        with open(last_file, "r") as f:
            return f.read()

    def __last_x_hour_file(self, hours: int):
        hours *= 3600
        file_list = []
        for file in os.listdir(self.__path):
            if file.startswith("check_") and os.path.getmtime(self.__path + '/' + file) > time.time() - hours:
                file_list.append(self.__path + file)
        self.__logger.info(f"Files from last {hours / 3600} hours: {file_list}")
        return file_list

    def __avg(self, hours: int):
        file_list = self.__last_x_hour_file(hours)
        cpu = []
        mem = []
        disk = []
        for file in file_list:
            with open(file, "r") as f:
                for line in f.readlines():
                    data = json.loads(line)
                    cpu.append(data["CPU"])
                    mem.append(data["RAM"])
                    disk.append(data["Disk"])
        dicoavg = {"CPU": str(sum(cpu) / len(cpu)), "RAM": str(sum(mem) / len(mem)), "Disk": str(sum(disk) / len(disk))}
        self.__logger.info(f"Average: {dicoavg}")
        return json.dumps(dicoavg)

    def get(self, metric, operation=None):
        if metric == "last":
            return self.__last()
        elif metric == "avg":
            if operation is None:
                self.__logger.error("Missing operation")
                exit(1)
            elif type(operation) is not int:
                self.__logger.error("Operation must be an integer")
                exit(1)
            else:
                return self.__avg(operation)
        else:
            self.__logger.error(f"Unknown metric: {metric}")
            exit(1)


if __name__ == '__main__':
    fire.Fire(Monitoring)
