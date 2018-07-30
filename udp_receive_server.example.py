#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# 本地开发使用

import socket
import time
import threading
import mysql.connector


def recvData(server_socket):
    index = 0
    while True:
        # data, addr = serversocket.recvfrom(1024)
        # if index > 0:
        # 	data_str = data.decode('utf-8')
        # 	agri_str = data_str.split(' ');
        # 	print(agri_str)
        # 	agri = list(map(int, agri_str))
        # 	print(agri)
        # else:
        # 	index = index + 1
        # 	continue
        # id = agri[0]
        # temperature = agri[1]
        # humanity = agri[2]
        # illumination = agri[3]
        # time = agri[4]

        data, addr = server_socket.recvfrom(1024)
        # index：when we first connect to guyu cloud platform，the cloud platform will return an bytes message:[iotxx:ok],
        # this message influence the data, so we filter this message.
        if index > 0:
            data_str = data.decode('utf-8')

            if data_str == 'ALIVE':
                print('bye')
                continue

            agri_str = data_str.split(',')
            print(agri_str)
        # agri = list(map(int, agri_str))
        # print(agri)
        else:
            index = index + 1
            continue

        # 树莓派编号、arduino编号、arduino类型（1山林，2水下，3田野）、土壤湿度、土壤温度、土壤盐度、
        # 土壤EC值、空气湿度、空气温度、二氧化碳浓度、光照强度、ph值、气压、风速、氧气浓度、时间
        Ard_number = agri_str[1]
        soil_Humidity = agri_str[3]
        soil_Temp = agri_str[4]
        soil_Salinity = agri_str[5]
        soil_EC = agri_str[6]
        air_Humidity = agri_str[7]
        air_Temp = agri_str[8]
        CO2_Concentration = agri_str[9]
        light_Intensity = agri_str[10]
        soil_PH = agri_str[11]
        air_Pressure = agri_str[12]
        wind_Speed = agri_str[13]
        O2_Concentration = agri_str[14]
        created = agri_str[15]

        # Inserting data into mysql
        conn = mysql.connector.connect(user='root', password='bupt626', database='iot_1')
        cursor = conn.cursor()
        # the type of data needed to insert into mysql must be String，or insert failed.
        query = "insert into " \
                "IoT_agri(Ard_number_id, soil_Humidity, " \
                "soil_Temp, soil_Salinity, soil_EC, air_Humidity, air_Temp, " \
                "CO2_Concentration, light_Intensity, soil_PH, air_Pressure, wind_Speed, " \
                "O2_Concentration, created) " \
                "values (%s, %s, %s, %s, %s, %s, " \
                "%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, [Ard_number, soil_Humidity, soil_Temp,
                               soil_Salinity, soil_EC, air_Humidity, air_Temp, CO2_Concentration,
                               light_Intensity, soil_PH, air_Pressure, wind_Speed, O2_Concentration, created])
        print(cursor.rowcount)
        conn.commit()
        cursor.close()
        conn.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.sendto(b'ep=23SSMC3PDDQ7T1N7&pw=845962', ('115.29.240.46', 6000))
recvThread = threading.Thread(target=recvData, args=(serversocket,))
recvThread.daemon = True
recvThread.start()
time.sleep(1)

while True:
    # serversocket.sendto(b'ddd',('115.29.240.46', 6000))
    time.sleep(2)
# recvThread.join()
# serversocket.close()
