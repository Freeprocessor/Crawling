import telepot
import requests
import pymysql
from bs4 import BeautifulSoup

# Crawling 
def Crawling():
    i = 19

    res = requests.get('https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258',
                       headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(res.content, 'html.parser')

    title_temp = soup.select('li > dl > .articleSubject')
    content_temp = soup.select('li > dl > .articleSummary')
    press_temp = soup.select('li > dl > .articleSummary > span.press')
    time_temp = soup.select('li > dl > .articleSummary > span.wdate')

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

# Save DataBase 
def SaveDB(title, href, content, press, time):
    conn = pymysql.connect(host='localhost', user='****', password='****',
                           db='naver_finance', charset='utf8')
    curs = conn.cursor()

    title = title.replace("<", "＜")
    title = title.replace(">", "＞")
    content = content.replace("<", "＜")
    content = content.replace(">", "＞")

    SaveDBi = 0
    sql = "select Title from article where Title = %s"
    curs.execute(sql, title)
    rows = curs.fetchall()
    for row in rows:
        temp1 = str(row[0])
        temp2 = str(title)
        if str(temp2) == str(temp1):
            print("Null")
            SaveDBi = 1
            break
        else:
            print("Else")

    if SaveDBi == 1:
        print("Already save to DB")
    else:
        sql = "insert into article(Title,href,Content,Press,Time) values(%s, %s, %s, %s, %s)"
        curs.execute(sql, (title, href, content, press, time))
        conn.commit()
        SandTelegram(title, href, content, press, time)

    conn.close()

# Sand by Telegram 
def SandTelegram(title, href, content, press, time):
    token = "****"
    mc = "****"
    bot = telepot.Bot(token)
    TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
    bot.sendMessage(mc, TeleMessage, 'HTML')

    mc = "****"
    bot = telepot.Bot(token)
    TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
    bot.sendMessage(mc, TeleMessage, 'HTML')

    mc = "****"
    bot = telepot.Bot(token)
    TeleMessage = "<a href=\"" + href + "\">" + title + "</a>" + "\n" + "\n" + content + "\n" + press + "\n" + time
    bot.sendMessage(mc, TeleMessage, 'HTML')


def main():
    Crawling()


if __name__ == '__main__':
    main()
