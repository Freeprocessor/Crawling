from Chatbot_Setting import *
import telepot
from telepot.loop import MessageLoop
import requests
import pymysql
from bs4 import BeautifulSoup

bot = telepot.Bot(TokenS)


def Chatbot(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    print(content_type, chat_type, chat_id, msg_date, msg_id)
    print(msg)
    conn = pymysql.connect(host='localhost', user=DBID, password=DBPassword,
                           db='sale', charset='utf8')
    curs = conn.cursor()
    if content_type == 'text':

        sql = "select count(userID) from user where userID = %s"
        curs.execute(sql, chat_id)
        userIDc = curs.fetchall()
        userID = userIDc[0][0]
        if msg['text'] == '등록':
            if 0 == userID:
                sql = "insert into user(userID, Permission, Subscribe) values(%s, %s ,%s)"
                curs.execute(sql, (chat_id, 0, 1))
                conn.commit()
                print("Save DataBase")
                bot.sendMessage(chat_id, "Welcome " + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
            else:
                print("Already save to DB")
                bot.sendMessage(chat_id, "Already registered.\n" + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
        if 1 == userID:
            if msg["text"] == '구독':
                sql = "select Subscribe from user where userID = %s"
                curs.execute(sql,  chat_id)
                Subscribes = curs.fetchall()
                Subscribe = Subscribes[0][0]
                if 0 == Subscribe:
                    sql = "update user set Subscribe = %s where userID = %s"
                    curs.execute(sql, (1,chat_id))
                    conn.commit()
                    print("Subscribe Success")
                    bot.sendMessage(chat_id, "Subscribe Success " + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
                else:
                    print("Already Subscribe")
                    bot.sendMessage(chat_id, "Already Subscribe.\n" + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
            elif msg['text'] == '구독취소':
                sql = "select Subscribe from user where userID = %s"
                curs.execute(sql,  chat_id)
                Subscribes = curs.fetchall()
                Subscribe = Subscribes[0][0]
                if 0 == Subscribe:
                    print("Already UnSubscribe")
                    bot.sendMessage(chat_id, "Already UnSubscribe.\n" + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
                else:
                    sql = "update user set Subscribe = %s where userID = %s"
                    curs.execute(sql, (0,chat_id))
                    conn.commit()
                    print("UnSubscribe Success")
                    bot.sendMessage(chat_id, "UnSubscribe Success " + msg['chat']['last_name'] + " " + msg['chat']['first_name'])
        # if chat_id == 1143142514:
        #     bot.sendMessage(chat_id, '(Echo)' + msg['text'])
        #     bot.sendMessage(753311691, '(공지)' + msg['text'])
        #     bot.sendMessage(1138918706, '(공지)' + msg['text'])
        # else:
        #     bot.sendMessage(chat_id, '(Echo)' + msg['text'])
        #     bot.sendMessage(1143142514, '(' + msg['chat']['first_name'] + ')' + msg['text'])


def main():
    MessageLoop(bot, Chatbot).run_forever()


if __name__ == '__main__':
    main()
