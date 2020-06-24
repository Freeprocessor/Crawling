from Chatbot_Setting import *
import telepot
import requests
import pymysql
from bs4 import BeautifulSoup


def Crawling():
    i = 19

    # 1) reqeusts 라이브러리를 활용한 HTML 페이지 요청
    # 1-1) res 객체에 HTML 데이터가 저장되고, res.content로 데이터를 추출할 수 있음
    res = requests.get('https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258',
                       headers={"User-Agent": "Mozilla/5.0"})

    # print(res.content)
    # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
    # 2-1) BeautifulSoup 파싱방법
    soup = BeautifulSoup(res.content, 'html.parser')

    # 3) 필요한 데이터 검색
    title_temp = soup.select('li > dl > .articleSubject')
    content_temp = soup.select('li > dl > .articleSummary')
    press_temp = soup.select('li > dl > .articleSummary > span.press')
    time_temp = soup.select('li > dl > .articleSummary > span.wdate')

    # 4) 필요한 데이터 추출
    while i > 0:
        print(title_temp[i].find('a')['title'])
        print("https://finance.naver.com" + title_temp[i].find('a')['href'])
        print(content_temp[i].get_text().lstrip().split('...')[0] + '...')
        print(press_temp[i].get_text())
        print(time_temp[i].get_text())
        print("\n")
        title = title_temp[i].find('a')['title']
        href = "https://finance.naver.com" + title_temp[i].find('a')['href']
        content = content_temp[i].get_text().lstrip().split('...')[0] + '...'
        press = press_temp[i].get_text()
        time = time_temp[i].get_text()
        SaveDB(title, href, content, press, time)
        i = i - 1
    # print("끝")


def SaveDB(title, href, content, press, time):
    conn = pymysql.connect(host='localhost', user=DBID, password=DBPassword,
                           db='naver_finance', charset='utf8')
    curs = conn.cursor()

    href = href.replace("§","%A1%")
    title = title.replace("<", "＜")
    title = title.replace(">", "＞")
    content = content.replace("<", "＜")
    content = content.replace(">", "＞")

    sql = "select count(Title) from article where Title = %s"
    # sql = "select Title from article where Title = %s"
    curs.execute(sql, title)
    # SandTelegram(title, href, content, press, time)
    rows = curs.fetchall()
    row = rows[0][0]

    if 0 == row :
        sql = "insert into article(Title,href,Content,Press,Time) values(%s, %s, %s, %s, %s)"
        curs.execute(sql, (title, href, content, press, time))
        conn.commit()
        SandTelegram(title, href, content, press, time)
    else:
        print("Already save to DB")

    conn.close()


def SandTelegram(title, href, content, press, time):
    conn = pymysql.connect(host='localhost', user=DBID, password=DBPassword,
                           db='naver_finance', charset='utf8')
    curs = conn.cursor()

    sql = "select userID from user"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        userID = row[0]
        sql = "select Subscribe from user where userID = %s"
        # temp = int(userID)
        curs.execute(sql, userID)
        Sub = curs.fetchall()
        if Sub[0][0] == 1:
            bot = telepot.Bot(TokenN)
            TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
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
    Crawling()


if __name__ == '__main__':
    main()