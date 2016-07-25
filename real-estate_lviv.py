# -*- coding: utf-8 -*-
import requests
import ast
import time
import MySQLdb
from bs4 import BeautifulSoup

URL_podobovo_kvartira='http://www.real-estate.lviv.ua/podobovo-kvartira/Lviv'
URL_sale_kvartira='http://www.real-estate.lviv.ua/sale-kvartira/Lviv'
URL_sale_kvartira_new='http://www.real-estate.lviv.ua/sale-kvartira/Lviv/%D0%BD%D0%BE%D0%B2%D0%BE%D0%B1%D1%83%D0%B4%D0%BE%D0%B2%D0%B8'
URL_sale_house='http://www.real-estate.lviv.ua/sale-house/Lviv'
URL_sale_house_cottage='http://www.real-estate.lviv.ua/sale-house/Lvivregion/%D0%BA%D0%BE%D1%82%D0%B5%D0%B4%D0%B6%D0%BD%D1%96-%D0%BC%D1%96%D1%81%D1%82%D0%B5%D1%87%D0%BA%D0%B0'
URL_sale_land='http://www.real-estate.lviv.ua/sale-land/Lviv'
URL_sale_commercialproperty='http://www.real-estate.lviv.ua/sale-commercialproperty/Lviv'
URL_orenda_kvartira='http://www.real-estate.lviv.ua/orenda-kvartira/Lviv'
URL_orenda_house='http://www.real-estate.lviv.ua/orenda-house/Lviv'
URL_orenda_commercialproperty='http://www.real-estate.lviv.ua/orenda-commercialproperty/Lviv'
URL_podobovo_house='http://www.real-estate.lviv.ua/podobovo-house/Lviv'

def test():
	url='http://www.real-estate.lviv.ua/519715-kvartira-podobovo-Lviv-Galickiy-Tamanska-vul.html'
	data=requests.get(url)
	data=data.content
	soup = BeautifulSoup(data)
	script=soup.find_all('script', type="text/javascript")
	print script[2].text[126:152]



def db_connect():
    try:
        db=MySQLdb.connect(host='localhost', user='root',passwd='123',db='orendatest')
        dbCursor=db.cursor()

    except MySQLdb.OperationalError:
    	# MySQLdb.OperationalError
        print 'Create db mestopars'
        db=MySQLdb.connect(host='localhost', user='root',passwd='123')
        dbCursor=db.cursor()
        dbCursor.execute('CREATE DATABASE mestopars DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci')

    dbCursor.execute('COMMIT')
    
    dbCursor.execute("SET NAMES utf8 COLLATE utf8_unicode_ci ;") #or utf8 or any other charset you want to handle
    dbCursor.execute("SET CHARACTER SET utf8;") #same as above
    return db

def make_url(nextPage=None):
	# response=URL+str(nextPage)
	return URL_sale_kvartira

def get_request(url):
	data = requests.get(url)
	dataHtml=data.content
	# print data.content
	return response

def get_linkAdver(url):
	data = requests.get(url)
	dataHtml=data.content
	soup = BeautifulSoup(dataHtml)
	countPage=soup.find('li', class_='last').text
	print countPage
	db=db_connect()
	cursor=db.cursor()
	for pageNumber in range(1,int(countPage)):
		print 'pageNumber= ' + str(pageNumber)
		url=URL_podobovo_kvartira
		url=url+'/p_'+str(pageNumber)
		print 'url=--------'+url 
		data = requests.get(url)
		print 'get_linkAdver data.url ' + data.url
		dataHtml=data.content
		# with open("dataHtml.html", 'w') as outfile:
		# 	outfile.write(dataHtml)
		# outfile.closed
		soup = BeautifulSoup(dataHtml)
		linkAdvertList=[]
		
		divAdvertList = soup.find_all('div', class_='row list-bordered preview_photo')
		for divAdvert in divAdvertList:
			try:
				link=divAdvert.find('div', class_='col-sm-12').a['href']
				print link
				print link[1:7]
				linkAdvertPage='http://www.real-estate.lviv.ua'+link
				linkAdvertPhone='http://www.real-estate.lviv.ua/ajax_show_phone_object/'+link[1:7]
				sql='''INSERT INTO page (link) VALUE ("%s")'''
				print sql%{'linkAdvertPage':linkAdvertPage,'linkAdvertPhone':linkAdvertPhone}
				cursor.execute(sql%{'linkAdvertPage':linkAdvertPage,'linkAdvertPhone':linkAdvertPhone})
				cursor.execute('COMMIT')
				# linkAdvertList.append({'linkAdvertPage':linkAdvertPage,'linkAdvertPhone':linkAdvertPhone})
			except AttributeError, e:
				print 'ERROR'  + e
	return done




 
def get_data(linkAdvertList=None):

	db=db_connect()
	cursor=db.cursor()
	cursor.execute('''SELECT link FROM page WHERE idpage<3000 ORDER BY idpage''')
	data=cursor.fetchall()
	# print(threading.current_thread().name)
	for v in data:
		linkAdvertList =dict(ast.literal_eval(v[0]))
		
		responseInfo=requests.get(linkAdvertList['linkAdvertPage'])
		dataHtml=responseInfo.content
		soup = BeautifulSoup(dataHtml)
		soup.text.encode('utf-8')
		name = soup.find('div', class_='col-xs-8 col-dense-right').a.text.encode('utf-8')
		print 'find name'
		tegInfoList = soup.find_all('li', class_='col-sm-6 col-dense-left')
		shortInfoList=[]
		for info in tegInfoList:
			shortInfoList.append(info.text.encode('utf-8'))
		print 'find short info'
		responsePhone = requests.get(linkAdvertList['linkAdvertPhone'])
		phoneStr = dict(ast.literal_eval(responsePhone.content))['message']
		phoneList=[]
		for i, v in enumerate(phoneStr):
			if v=='+':
				phoneList.append(phoneStr[i:i+17])
		print 'find phone'
		descr = soup.find_all('div', class_='col-md-8')[1].find_all('div', class_='col-xs-12')[3].text.encode('utf-8')
		print 'find desc'
		script=soup.find_all('script', type="text/javascript")
		# print script[2].text
		coordStart=script[2].text.find('[')
		coordEnd=script[2].text.find(']')+1
		# print coordStart,coordEnd
		coord=script[2].text[coordStart:coordEnd]
		coordList=list(ast.literal_eval(coord))
		# print coordList
			# with open("log.txt", 'w') as logfile:
			# 	logfile.write(name.encode('utf-8'))
			# 	logfile.write(str(shortInfoList))
			# 	logfile.write(str(phoneList))
			# 	logfile.write(descr.encode('utf-8'))
			# logfile.closed
		sql='''INSERT INTO orendaPodobovo (name,shortInfo,phone,descr,coord) VALUE ("%s","%s","%s","%s","%s")'''%(str(name),str(shortInfoList),str(phoneList),str(descr),str(coordList))
		try:
			cursor.execute(sql)
			cursor.execute('COMMIT')
		except Exception, e:
			print e

				
	print'---------------------------------------------------------------------------------------------------------------------------------------------'
		

def main():
	start = time.time()
	get_linkAdver(URL_podobovo_kvartira)
	get_data()
	print('Entire job took:',time.time() - start)

	

if __name__ == '__main__':
	main()