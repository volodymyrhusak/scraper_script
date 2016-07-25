# -*- coding: utf-8 -*-
import requests
import os
import CodingInfo
import MySQLdb
import base64
from bs4 import BeautifulSoup
from PIL import Image

#print "encoding data--------" + CodingInfo.get_codepage(data)
#git remote add origin https://github.com/volodymyrhusak/pars-kinopoisk.git
#git push -u origin master
def db_connect():
    try:
        db=MySQLdb.connect(host='localhost', user='root',passwd='123',db='lodkotest')
        dbCursor=db.cursor()

    except MySQLdb.OperationalError:
        print 'Create db lodkotest'
        db=MySQLdb.connect(host='localhost', user='root',passwd='123')
        dbCursor=db.cursor()
        dbCursor.execute('CREATE DATABASE lodkotest DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci')

    dbCursor.execute('COMMIT')
    
    dbCursor.execute("SET NAMES utf8 COLLATE utf8_unicode_ci ;") #or utf8 or any other charset you want to handle
    dbCursor.execute("SET CHARACTER SET utf8;") #same as above


    
    try:
        dbCursor.execute('SELECT 1 FROM kinopoiskfilm')
    except MySQLdb.ProgrammingError:
        print  'CREATE TABLE kinopoiskfilm'
        dbCursor.execute('''CREATE TABLE kinopoiskfilm (
            idkinopoiskfilm INT PRIMARY KEY AUTO_INCREMENT, 
            name VARCHAR(20), 
            slogan VARCHAR(100),
            descr VARCHAR(1000),
            year VARCHAR(15),
            studio VARCHAR(1000)
            )DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci
            ''')

     
    try:
        dbCursor.execute('SELECT 1 FROM filmimage')
    except MySQLdb.ProgrammingError:
        print  'CREATE TABLE filmimage'
        dbCursor.execute('CREATE TABLE filmimage (idfilmimage INT PRIMARY KEY AUTO_INCREMENT, imagefilm LONGBLOB, idkinopoiskfilm INT,reviewdescr LONGTEXT)DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci')

    # try:
    #     dbCursor.execute('SELECT 1 FROM review')
    # except MySQLdb.ProgrammingError:
    #     print  'CREATE TABLE review'
    #     dbCursor.execute('CREATE TABLE review (idreview INT PRIMARY KEY AUTO_INCREMENT, idkinopoiskfilm INT,reviewdescr LONGTEXT)DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci')
    
    return db
def get_studio(urlFilm):
    urlListStudio=urlFilm+'studio/'
    urlStudioFilmDict={}
    response = requests.get(urlListStudio)
    response.encoding='UTF-8'
    response.text.encode('utf-8')
    htmlListStudio=response.content
    soup=BeautifulSoup(htmlListStudio)
    divListStudio=soup.find('div', style="margin-left: 64px; text-align: left")
    studioTable=divListStudio.find_all('table')[0]
    studio=studioTable.find_all('td')
    for td in studio:
        if td.a:           
            urlStudioFilmDict[td.a.text.encode('utf-8')]='http://www.kinopoisk.ru/'+td.a['href']

    print urlStudioFilmDict
    return ','.join(urlStudioFilmDict.keys())




def enter_film_name():
    serch_name=str(raw_input('Enter film name or if you want enter studio click [ENTER]: '))
    if serch_name:
        #serch_name='Long men fei jia'
        serch_name=serch_name.replace(' ','+')
        print 'serch_name-----'+serch_name
        return serch_name
    else:
        studio=str(raw_input('Enter studio: '))
        year=str(raw_input('Enter year: '))
        return select_film(studio,year)

def select_film(studio,year):
    # studio="China Film Co."
    # year="2014"
    db=db_connect()
    dbCursor=db.cursor()
    dbCursor.execute('''select k.name,f.imagefilm, f.reviewdescr 
                        from kinopoiskfilm k 
                        join filmimage f on f.idkinopoiskfilm=k.idkinopoiskfilm 
                        where k.studio like "%'''+studio+'''%"  and k.year="'''+year+'''"''')

    for film in dbCursor.fetchall():
        print film[0]#+'/n'+film[1]+'/n'+film[2]

def make_url(filmName=None):
    start_url='http://www.kinopoisk.ru/index.php?first=no&what=&kp_query='
    if filmName:
        return start_url+filmName
    else:
        enterFilmName=enter_film_name()
        if enter_film_name:
            return start_url+enterFilmName

def get_id_film(html):
     soup = BeautifulSoup(html)
     div=soup.find('div',class_='element most_wanted')
     p=div.find('p',class_='name')
     id_film=p.a['href']
     print id_film
     return id_film

     

def parse(html):
    year=u'год'
    slogan=u'слоган'


# Ceate soup
    soup = BeautifulSoup(html)
    


# get film name
    divName =soup.find('div', id='headerFilm')
    filmNameRus = divName.h1.text.encode('UTF-8')
   
# get film descr
    film_descr=soup.find('div', class_="block_left_padtop").find('div', class_="brand_words").text.encode('UTF-8')

# get film year and slogan
    infoDiv=soup.find("div" ,id="infoTable" )
    infoTable= infoDiv.find_all('tr')

    for tr in infoTable:
        a=tr.td.text
        if a ==year:
            print 'a ==year'
            film_year= tr.div.a.text
        elif a ==slogan:
            print 'a ==slogan'
            film_slogan= tr.find_all('td')[1].text.encode('UTF-8')


# get review
    film_res=soup.find_all("div" ,class_="reviewItem userReview")
    review =str()
    for data in film_res:
        review=review+data.find('span', class_='_reachbanner_').text.encode('UTF-8')
    img_url=soup.find('div' ,class_="film-img-box").img['src']
    img_requests=requests.get(img_url).content




    return filmNameRus,film_year,film_slogan,film_descr,img_requests,review


# function insert data into database
def insert_data(db,data,studio):
    filmNameRus=data[0]
    film_year=data[1]
    film_slogan=data[2]
    film_descr=data[3]
    img_requests=base64.b64encode(data[4])
    film_res=data[5]
    dbCursor=db.cursor()
    
    dbCursor.execute('INSERT INTO kinopoiskfilm (name,slogan,descr,year,studio)VALUE("%s","%s","%s","%s","%s")'%(filmNameRus,film_slogan,film_descr,str(film_year),studio))
    dbCursor.execute('COMMIT')


    dbCursor.execute('SELECT max(idkinopoiskfilm) FROM kinopoiskfilm WHERE name="%s"'%(filmNameRus))
    idkinopoiskfilm=int(dbCursor.fetchone()[0])
    
    dbCursor.execute('INSERT INTO filmimage (imagefilm,idkinopoiskfilm,reviewdescr)VALUE("%s",%s,"%s")'%(img_requests,str(idkinopoiskfilm),film_res))
    dbCursor.execute('COMMIT')


    # for review in film_res:
    #     print idkinopoiskfilm
    #     dbCursor.execute('INSERT INTO review (idkinopoiskfilm,reviewdescr) VALUE (%s,"%s")'%(str(idkinopoiskfilm),review))
    # dbCursor.execute('COMMIT')
    db.close()

# save image in file
def save_image (filmNameRus,soup):
    current_directory=os.getcwd ()
    kino_folder =os.listdir (os.path.join(current_directory,'kinopoisk'))
   
    save_directory=os.path.join('kinopoisk',filmNameRus)
    os.mkdir (save_directory)

    img_url=soup.find('div' ,class_="film-img-box").img['src']
    img_requests=requests.get(img_url)
    image=open (os.path.join(save_directory,filmNameRus+'.jpg'),'wb')
    image.write(img_requests.content)
    image.close()
    print "_________________________________________image save_____________________________________"


def main():
    URL=make_url()
    if URL: 
        print URL
        response = requests.get(URL)
        response.encoding='UTF-8'
        print "response code-----------------------------------"+ str(response.status_code)
        response.text.encode('utf-8')
        print "encoding response.text-------------------------------------" + CodingInfo.get_codepage(response.text)
        data=response.content
            
        
        if URL==response.url:
            print "-------if URL==response.url"
            print "-------parse serch data"
            
            id_film=get_id_film(data)       
            URL='http://www.kinopoisk.ru/'+id_film
            print 'URL:---------- '+URL 
            response = requests.get(URL)
            response.encoding='UTF-8'
            print 'response.url:-------- '+response.url
            response.text.encode('utf-8')
            data=response.content
                
            print "-----------parse main data"
            insert_data(db_connect(),parse(data),get_studio(response.url))

            
        else:
            print "------------parse main data"
            insert_data(db_connect(),parse(data),get_studio(response.url))
            

    print '_________________________________________END_____________________________________'



        

if __name__ == '__main__':
    print '____________________________________________________START PARSER ____________________________________________________'
    main()