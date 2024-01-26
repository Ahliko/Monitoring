#!/usr/bin/env python3
"""
Monitoring class
"""
import json
import os
import socket
import sys
import time
import uuid
from datetime import datetime
from logging import DEBUG, Logger, FileHandler

import colorlog
import psutil
from fire import Fire


class Monitoring:
    """
    Monitoring class

    Usage:
    monit = Monitoring()
    monit.check()
    monit.list()
    monit.get("last")
    monit.get("avg", 24)
    """

    def __init__(self):
        self.__logger = self.__get_logger()
        self.__path = "/var/monit/"

    @staticmethod
    def __get_logger() -> Logger:
        logger = colorlog.getLogger()
        logger.setLevel(DEBUG)
        file_handler = FileHandler("/var/log/monit.log", "w", "utf-8")
        file_handler.setLevel(DEBUG)
        stream_handler = colorlog.StreamHandler()
        stream_handler.setLevel(DEBUG)

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        return logger

    def list(self):
        """
        List all files in /var/monit
        :return: list of files
        """
        lst = []
        for file in os.listdir(self.__path):
            if file.startswith("check_"):
                self.__logger.info(file)
                lst.append(file)
        return lst

    def __check_cpu(self):
        cpu_percent = psutil.cpu_percent()
        self.__logger.info("CPU usage: %s", str(cpu_percent) + "%")
        return cpu_percent

    def __check_ram(self):
        ram_percent = psutil.virtual_memory().percent
        self.__logger.info("RAM usage: %s", str(ram_percent) + "%")
        return ram_percent

    def __check_disk(self):
        disk_percent = psutil.disk_usage("/").percent
        self.__logger.info("Disk usage: %s", str(disk_percent) + "%")
        return disk_percent

    def __check_port(self):
        if not os.path.exists(f"{self.__path}/monit_conf.json"):
            os.system(f"touch {self.__path}/monit_conf.json")
        with open(f"{self.__path}/monit_conf.json", encoding="utf-8") as file:
            try:
                data = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                data = {"CHECK_PORTS": []}
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return [
            sock.connect_ex(("127.0.0.1", port)) == 0 for port in data["CHECK_PORTS"]
        ]

    def check(self):
        """
        Check CPU, RAM, Disk and ports
        :return: None
        """
        date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        myjson = {
            "Date": date,
            "ID": str(uuid.uuid4()),
            "CPU": self.__check_cpu(),
            "RAM": self.__check_ram(),
            "Disk": self.__check_disk(),
            "Port": self.__check_port(),
        }
        if os.path.exists(f"{self.__path}check_{date}.json"):
            with open(f"{self.__path}check_{date}.json", "a", encoding="utf-8") as file:
                self.__logger.info("Ecriture dans : %scheck_%s.json", self.__path, date)
                file.write("\n")
                file.write(json.dumps(myjson))
        else:
            with open(f"{self.__path}check_{date}.json", "a", encoding="utf-8") as file:
                self.__logger.info("Ecriture dans : %scheck_%s.json", self.__path, date)
                file.write(json.dumps(myjson))

    def __last(self):
        last_file = max(
            list(
                self.__path + f
                for f in os.listdir(self.__path)
                if f.startswith("check_")
            ),
            key=os.path.getctime,
        )
        self.__logger.info("Last file: %s", last_file)
        with open(last_file, encoding="utf-8") as file:
            return file.read()

    def __last_x_hour_file(self, hours: int):
        hours *= 3600
        file_list = []
        for file in os.listdir(self.__path):
            if (
                file.startswith("check_")
                and os.path.getmtime(self.__path + "/" + file) > time.time() - hours
            ):
                file_list.append(self.__path + file)
        self.__logger.info("Files from last %s hours: %s", hours / 3600, file_list)
        return file_list

    def __avg(self, hours: int):
        file_list = self.__last_x_hour_file(hours)
        self.__logger.debug("Files from last %s hours: %s", hours, file_list)
        if len(file_list) == 0:
            self.__logger.warning("No file found for this period")
            return json.dumps({"CPU": "0", "RAM": "0", "Disk": "0"})
        cpu = []
        mem = []
        disk = []
        for file in file_list:
            with open(file, encoding="utf-8") as myfile:
                for line in myfile.readlines():
                    line = line.strip()
                    self.__logger.debug("File: %s", line)
                    data = json.loads(line)
                    cpu.append(data["CPU"])
                    mem.append(data["RAM"])
                    disk.append(data["Disk"])
        dico_avg = {
            "CPU": str(sum(cpu) / len(cpu)),
            "RAM": str(sum(mem) / len(mem)),
            "Disk": str(sum(disk) / len(disk)),
        }
        self.__logger.info("Average: %s", dico_avg)
        return json.dumps(dico_avg)

    def get(self, metric, operation=None):
        """
        Get last file or average of last x hours
        :param metric:
        :param operation:
        :return:
        """
        if metric == "last":
            return self.__last()
        if metric == "avg":
            if operation is None:
                self.__logger.error("Missing operation")
                sys.exit(1)
            elif not isinstance(operation, int):
                self.__logger.error("Operation must be an integer")
                sys.exit(1)
            else:
                return self.__avg(operation)
        else:
            self.__logger.error("Unknown metric: %s", metric)
            sys.exit(1)


if __name__ == "__main__":
    Fire(Monitoring)
