#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# 本地开发使用

import socket, time, threading
import mysql.connector

def recvData(serversocket):
	
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


		data, addr = serversocket.recvfrom(1024)
		# index：when we first connect to guyu cloud platform，the cloud platform will return an bytes message:[iotxx:ok],
		# this message influence the data, so we filter this message.
		if index > 0:	
			data_str = data.decode('utf-8')

			if data_str == 'ALIVE':
				print('bye')
				continue
			
			agri_str = data_str.split(',');
			print(agri_str)
			# agri = list(map(int, agri_str))
			# print(agri)
		else:
			index = index + 1
			continue

		#arduino编号、arduino类型（1山林，2水下，3田野）、土壤湿度、土壤温度、土壤盐度、
		#土壤EC值、空气湿度、空气温度、二氧化碳浓度、光照强度、ph值、气压、风速、氧气浓度、时间
		id = agri_str[0]
		kind = agri_str[1]
		id_int = int(id)	# 将收到的字符串类型转换成int类型
		kind_int = int(kind)

		# 判断arduino的种类，将对应的数据分别存入到对应的数据表中

		# 田野
		if kind_int == 3:
			soil_Temperature = agri_str[2]
			soil_Humidity = agri_str[3]
			soil_Conductivity = agri_str[5]
			soil_Salinity = agri_str[4]
			air_Temperature = agri_str[7]
			air_Humidity = agri_str[6]
			carbonDioxide_Concentration = agri_str[8]
			soil_PH = agri_str[10]
			light_Intensity = agri_str[9]
			oxygen_Concentration = agri_str[13]
			air_Pressure = agri_str[11]
			created = agri_str[14]
			# Inserting data into mysql
			conn = mysql.connector.connect(user='xxx', password='xxx', database='iot_1')
			cursor = conn.cursor()
			# the type of data needed to insert into mysql must be String，or insert failed.
			cursor.execute('insert into IoT_field (number, soil_Temperature, soil_Humidity, soil_Conductivity, soil_Salinity, air_Temperature, air_Humidity, carbonDioxide_Concentration, soil_PH, light_Intensity, oxygen_Concentration, air_Pressure, created) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)', 
						[id, soil_Temperature, soil_Humidity, soil_Conductivity, soil_Salinity, air_Temperature, air_Humidity, carbonDioxide_Concentration, soil_PH, light_Intensity, oxygen_Concentration, air_Pressure, created ])
			print(cursor.rowcount)
			conn.commit()
			cursor.close()
			conn.close()


		#arduino编号、arduino类型（1山林，2水下，3田野）、土壤湿度、土壤温度、土壤盐度、
		#土壤EC值、空气湿度、空气温度、二氧化碳浓度、光照强度、ph值、气压、风速、氧气浓度、时间
		# 水下
		if kind_int == 2:
			liquid_Temperature = agri_str[2]
			liquidDissolved_OxygenConcentration = agri_str[8]
			liquid_PH = agri_str[10]
			light_Intensity = agri_str[9]
			air_Pressure = agri_str[11]
			created = agri_str[14]
			# Inserting data into mysql
			conn = mysql.connector.connect(user='xxx', password='xxx', database='iot_1')
			cursor = conn.cursor()
			# the type of data needed to insert into mysql must be String，or insert failed.
			cursor.execute('insert into IoT_pond (number, liquid_Temperature, liquidDissolved_OxygenConcentration, liquid_PH, light_Intensity, air_Pressure, created) values (%s, %s, %s, %s, %s, %s, %s)', 
						[id, liquid_Temperature, liquidDissolved_OxygenConcentration, liquid_PH, light_Intensity, air_Pressure, created])
			print(cursor.rowcount)
			conn.commit()
			cursor.close()
			conn.close()


		#arduino编号、arduino类型（1山林，2水下，3田野）、土壤湿度、土壤温度、土壤盐度、
		#土壤EC值、空气湿度、空气温度、二氧化碳浓度、光照强度、ph值、气压、风速、氧气浓度、时间
		# 山林
		if kind_int == 1:
			soil_Temperature = agri_str[2]
			soil_Humidity = agri_str[3]
			soil_Conductivity = agri_str[5]
			soil_Salinity = agri_str[4]
			air_Temperature = agri_str[7]
			air_Humidity = agri_str[6]
			carbonDioxide_Concentration = agri_str[8]
			soil_PH = agri_str[10]
			light_Intensity = agri_str[9]
			wind_Speed = agri_str[12]
			air_Pressure = agri_str[11]
			created = agri_str[14]
			# Inserting data into mysql
			conn = mysql.connector.connect(user='xxx', password='xxx', database='iot_1')
			cursor = conn.cursor()
			# the type of data needed to insert into mysql must be String，or insert failed.
			cursor.execute('insert into IoT_forest (number, soil_Temperature, soil_Humidity, soil_Conductivity, soil_Salinity, air_Temperature, air_Humidity, carbonDioxide_Concentration, soil_PH, light_Intensity, wind_Speed, air_Pressure, created) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)', 
						[id, soil_Temperature, soil_Humidity, soil_Conductivity, soil_Salinity, air_Temperature, air_Humidity, carbonDioxide_Concentration, soil_PH, light_Intensity, wind_Speed, air_Pressure, created])
			print(cursor.rowcount)
			conn.commit()
			cursor.close()
			conn.close()



		# temperature = agri_str[1]
		# humanity = agri_str[2]
		# illumination = agri_str[3]
		# time = agri_str[4]
		# print(id)
		# print(type(id))
		# print(kind)
		# print(type(kind))


	# 	Inserting data into mysql
	# 	conn = mysql.connector.connect(user='root', password='Yth2009', database='iot_1')
	# 	cursor = conn.cursor()

	# 	# the type of data needed to insert into mysql must be String，or insert failed.
	# 	cursor.execute('insert into IoT_agri (id, temperature, humanity, illumination, time) values (%s, %s, %s, %s, %s)', 
	# 					[id, temperature, humanity, illumination, time])
	# 	print(cursor.rowcount)
	# 	conn.commit()
	# 	cursor.close()
	
	# conn.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.sendto(b'ep=xxxx&pw=xxxx', ('115.29.240.46', 6000))
recvThread = threading.Thread(target=recvData, args=(serversocket,))
recvThread.daemon = True
recvThread.start()
time.sleep(1)


while True:
	# serversocket.sendto(b'ddd',('115.29.240.46', 6000))
	time.sleep(2)
recvThread.join()
serversocket.close()





