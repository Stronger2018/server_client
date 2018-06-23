#!/usr/bin/python3 
#coding=utf-8

from signal import *
from socket import *
import pymysql
from time import *
import sys
import os

DICT_TEXT = "./dict.txt"


def do_child(connfd,db):
    while True:
        msg = connfd.recv(128).decode()
        print("msg : ",msg)

        if msg[0] == 'R':
            do_register(connfd,msg,db)

        if msg[0] == 'L':
            do_login(connfd,msg,db)

        if msg[0] == 'Q':
            do_query(connfd,msg,db)

        if msg[0] == 'H':
            do_history(connfd,msg,db)

        if msg[0] == 'E':
            sys.exit(0)
    return


def do_register(connfd,msg,db):
    print("in register.......")
    cursor = db.cursor()
    s = msg.split(' ')
    name = s[1]
    passwd = s[2]

    sql = "select * from user where name = '%s'"%name
    cursor.execute(sql)
    data = cursor.fetchone()

    if data != None:
        connfd.send("FALL".encode())
        return

    sql = "insert into user values ('%s','%s')"%(name,passwd)

    try:
        cursor.execute(sql)
        db.commit()
        connfd.send('OK'.encode())
    except:
        connfd.send("FALL".encode())
        db.rollback()
        return
    else:
        print("register OK !")


def do_login(connfd,msg,db):
    print("in login.......")
    cursor = db.cursor()
    s = msg.split(' ')
    name = s[1]
    passwd = s[2]

    try:
        sql = "select * from user where name = '%s' and passwd = '%s'"%(name,passwd)
        cursor.execute(sql)
        data = cursor.fetchone()
        print(data)
    except:
        pass

    if data == None:
        connfd.send("FALL".encode())
    else:
        connfd.send('OK'.encode())

    return
    

def do_query(connfd,msg,db):
    print("in query.......")
    cursor = db.cursor()
    s = msg.split(' ')
    word = s[1]
    name = s[2]

    try:
        f = open(DICT_TEXT,'r')
    except:
        print("open failed")
        connfd.send('FALL'.encode())
        return

    connfd.send('OK'.encode())
    sleep(0.1)
    while True:
        buf = f.readline()
        f.flush()
        temp = buf.split(' ')
        if temp[0] > word:
            connfd.send("not found".encode())
            f.close()
            break

        if temp[0] == word:

            msg = buf
            connfd.send(msg.encode())

            insert_history(db,word,name)

            f.close()
            return


def do_history(connfd,msg,db):
    print("in history.......")
    cursor = db.cursor()
    s = msg.split(' ')
    name = s[1]

    sql = "select * from hist where name = '%s'"%name

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        connfd.send('OK'.encode())
    except:
        print("history failed")
        db.rollback()
        connfd.send('FALL'.encode())

    for row in results:
        name = row[0]
        word = row[1]
        time = row[2]
        sleep(0.1)
        connfd.send(("%s  %s  %s"%(name,word,time)).encode())
   
    sleep(0.1)
    connfd.send('over'.encode())
    return


def insert_history(db,word,name):
    time = ctime()
    cursor = db.cursor()
    sql = "insert into hist values('%s','%s','%s')"%(name,word,time)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("sorry insert failed")
        db.rollback()
        return


def main():
    signal(SIGCHLD,SIG_IGN)
    
    db = pymysql.connect('localhost','root','123456','dict')

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    sockfd = socket()
    sockfd.bind((HOST,PORT))
    sockfd.listen(5)

    while True:
        try:
            connfd,addr = sockfd.accept()
            print("connect addr : ",addr)
        except KeyboardInterrupt:
            raise
        except:
            continue

        pid =  os.fork()
        
        if pid < 0:
            print("create child process failed")
            connfd.close()
            continue
        elif pid == 0:
            sockfd.close()
            do_child(connfd,db)
        else:
            connfd.close()
            continue

    db.close()
    sockfd.close()
    sys.exit(0)


if __name__ == "__main__":
    main()

