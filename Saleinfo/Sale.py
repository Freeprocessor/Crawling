import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from Chatbot_Setting import *
import telepot
import requests
import pymysql
from bs4 import BeautifulSoup


def Crawling(site):

    if site=="Ppomppu":
        i = 19
        res = requests.get('http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu',
                        headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(res.content, 'html.parser')

        title_temp = soup.select('tr > td.list_vspace > table font')
        href_temp = soup.select('tr > td.list_vspace > table tr > td > a')
        classification_temp = soup.select('tr > td.han4 > nobr')
        time_temp = soup.select('tr > td.eng > nobr')

        while i > 0:
            print(title_temp[i].get_text())
            print("http://www.ppomppu.co.kr/zboard/" + href_temp[i*2]['href'])
            print(classification_temp[i].get_text())
            print("Ppomppu")
            print(time_temp[i].get_text())
            print("\n")
            title = title_temp[i].get_text()
            href = "http://www.ppomppu.co.kr/zboard/" + href_temp[i*2]['href']
            classification = classification_temp[i].get_text()
            site = "Ppomppu"
            time = time_temp[i].get_text()
            SaveDB(title, href, classification, site, time)
            i = i - 1
    elif site=="QuasarZone":
        i = 29
        res = requests.get('https://www.quasarzone.com/bbs/qb_saleinfo',
                        headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(res.content, 'html.parser')

        title_temp = soup.select('tr > td > p.tit > a.subject-link')
        href_temp = soup.select('tr > td > p.tit > a.subject-link')
        time_temp = soup.select('tr > td > span.date')

        while i > 0:
            print(title_temp[i].get_text().strip())
            print("https://www.quasarzone.com" + href_temp[i]['href'])
            print("None")
            print("QuasarZone")
            print(time_temp[i].get_text().strip())
            print("\n")
            title = title_temp[i].get_text().strip()
            href = "https://www.quasarzone.com" + href_temp[i]['href']
            classification = "None"
            site = "QuasarZone"
            time = time_temp[i].get_text().strip()
            SaveDB(title, href, classification, site, time)
            i = i - 1
    elif site=="Cooln":
        i = 24
        res = requests.get('http://www.coolenjoy.net/bbs/jirum',
                        headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(res.content, 'html.parser')

        title_temp = soup.select('tbody > tr > td.td_subject > a')
        href_temp = soup.select('tbody > tr > td.td_subject > a')
        classification_temp = soup.select('tbody > tr > td.td_num')
        time_temp = soup.select('tbody > tr > td.td_date')

        while i > 0:
            print(title_temp[i].get_text().split('댓글')[0].strip())
            print(href_temp[i]['href'])
            print(classification_temp[i].get_text().strip())
            print("Cooln")
            print(time_temp[i].get_text().strip())
            print("\n")
            title = title_temp[i].get_text().split('댓글')[0].strip()
            href = href_temp[i]['href']
            classification = classification_temp[i].get_text().strip()
            site = "Cooln"
            time = time_temp[i].get_text().strip()
            SaveDB(title, href, classification, site, time)
            i = i - 1


def SaveDB(title, href, classification, site, time):
    conn = pymysql.connect(host='localhost', user=DBID, password=DBPassword,
                           db='sale', charset='utf8')
    curs = conn.cursor()

    sql = "select count(Title) from sale_info where Title = %s"
    # sql = "select Title from article where Title = %s"
    curs.execute(sql, title)
    # SandTelegram(title, href, content, press, time)
    rows = curs.fetchall()
    row = rows[0][0]

    if 0 == row :
        sql = "insert into sale_info(Title,Href,Classification,Site,Time) values(%s, %s, %s, %s, %s)"
        curs.execute(sql, (title, href, classification, site, time))
        conn.commit()
        SandTelegram(title, href, classification, site, time)
    else:
        print("Already save to DB")

    conn.close()


def SandTelegram(title, href, classification, site, time):
    conn = pymysql.connect(host='localhost', user=DBID, password=DBPassword,
                           db='sale', charset='utf8')
    curs = conn.cursor()

    sql = "select userID from user"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        userID = row[0]
        sql = "select Subscribe from user where userID = %s"
        curs.execute(sql, userID)
        Sub = curs.fetchall()
        if Sub[0][0] == 1:
            bot = telepot.Bot(TokenS)
            TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + classification + "\n" + site + "\n" + time
            bot.sendMessage(int(userID), TeleMessage, 'HTML')


    # mc = "753311691"
    # bot = telepot.Bot(token)
    # TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
    # bot.sendMessage(mc, TeleMessage, 'HTML')

    # mc = "1138918706"
    # bot = telepot.Bot(token)
    # TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
    # bot.sendMessage(mc, TeleMessage, 'HTML')


def main():
    Crawling("Ppomppu")
    Crawling("QuasarZone")
    Crawling("Cooln")


if __name__ == '__main__':
    main()