import numpy as np
import traceback
import requests
import sys
import urllib3
import json
from datetime import *
from bs4 import BeautifulSoup
class Aduana():

	headers = None
	def __init__(self):
		print("__init__")
	#in  YYYY-MM-DD
	def getFormatDate(self,date):
		
		month = date.split('-')[1]
		day = date.split('-')[2]
		year = date.split('-')[0]
		return datetime(int(year),int(month),int(day))

	#in  dd/mm/yy
	def getFormatCubanDate(self,date):
		day = date.split('/')[0]
		month = date.split('/')[1]
		year = "20"+date.split('/')[2]
		return datetime(int(year),int(month),int(day))

	def getContent(self,dateFrom,dateTo,cityFrom,cityTo):
		try:
			cityFrom = cityFrom.upper()
			print('getContent('+dateFrom+','+dateTo+','+cityFrom+','+cityTo+')')
			TARGET = 'http://www.aduana.cu/api/api_aceptados.php'
			data = {'aeropuerto':cityTo}
			
			#Production 
			http = urllib3.PoolManager()
			r = http.request('POST',TARGET,fields=data)
			soup = BeautifulSoup(r.data,"html.parser")

			#Test porpuses
			#test = open('test.html')
			#soup = BeautifulSoup(test,"html.parser")
			
			#cel index
			flighNumer = 1
			fromCityCel = 2
			originDateCel = 3
			toCityCel = 4
			destinationDateCel = 5
			passengers = 7

			#the 2 first rows are the header
			initialRow = 2
			headerSkiperCont = 0
			rows = ""
			
			#even = flighNumber | odd = TotalPassenger
			chartData = list()
			dateFrom = self.getFormatDate(dateFrom)
			dateTo = self.getFormatDate(dateTo)
			soup = soup.find("div")	
			for i,row in enumerate(soup.findAll("tr")):
				#skip header of the table
				if headerSkiperCont < initialRow:
					headerSkiperCont += 1
					continue

				#cuba format dd/mm/yy
				originDate=self.getFormatCubanDate(row.findAll("th")[originDateCel].text.split(" ")[0])
				destinationDate=self.getFormatCubanDate(row.findAll("th")[destinationDateCel].text.split(" ")[0])
			
				if(dateFrom<= originDate or dateFrom <= destinationDate) and (dateTo>=originDate or dateTo >=destinationDate):
					if cityFrom !='':
						if row.findAll("th")[fromCityCel].text == str(cityFrom):
							rows += str(row)
							#try catch placed to make sure the collection of the chartData won't kill the core process
							try:
								if row.findAll("th")[passengers].text != '-':
									number = row.findAll("th")[flighNumer].text
									passengersCount = row.findAll("th")[passengers].text.split(" ")[0]
									if dateFrom != dateTo:
										date = row.findAll("th")[destinationDateCel].text.split(" ")[0]
										chartData.append([number,passengersCount,date])
									else:
										chartData.append([number,passengersCount])

									"""
										This will check and agroup the count of the passengers by flight number
										but the original table has repeated data so, it won't be precise 
									if len(chartData)!= 0 and number in chartData[0]:
										chartData[chartData.index(numeber)]+=passengersCount
									else:
										chartData.append([number,passengersCount])
									"""
							except Exception as e:	
								print(e)
								traceback.print_tb(e.__traceback__)
					else:						
						rows+=str(row)
						#try catch placed to make sure the collection of the chartData won't kill the core process
						try:
							if row.findAll("th")[passengers].text != '-':
								number = row.findAll("th")[flighNumer].text
								passengersCount = row.findAll("th")[passengers].text.split(" ")[0]
								if dateFrom != dateTo:
									date = row.findAll("th")[destinationDateCel].text.split(" ")[0]
									chartData.append([number,passengersCount,date])
								else:
									chartData.append([number,passengersCount])

								"""
									This will check and agroup the count of the passengers by flight number
									but the original table has repeated data so, it won't be precise 
								if len(chartData)!= 0 and number in chartData[0]:
									chartData[chartData.index(numeber)]+=passengersCount
								else:
									chartData.append([number,passengersCount])
								"""
						except Exception as e:	
							print(e)
							traceback.print_tb(e.__traceback__)
							
		except Exception as e:
			print(e)
			traceback.print_tb(e.__traceback__)

		return json.dumps({"rows":rows,"chartData":chartData,"cities":self.getCityFullName(cityFrom,cityTo)})


	def getCityFullName(self,origin,destination):
		try:
			print('getCityFullName('+origin+','+destination+')')
			file = open('app/templates/airportCodes.html')
			soup = BeautifulSoup(file,"html.parser")
			
			if origin is not '':
				parent =soup.find(text=origin.upper()).parent
				before = parent.find_previous_siblings("th")[0]
				origin = before.text + " - "
			
			parent =soup.find(text=destination.upper()).parent
			before = parent.find_previous_siblings("th")[0]
			destination = before.text
		except Exception as e:
			print(e)
			traceback.print_tb(e.__traceback__)

		return json.dumps({"origin":origin,"destination":destination})
