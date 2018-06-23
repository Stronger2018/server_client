#!/usr/bin/python
#coding=utf-8

from socket import *
import MySQLdb
import time

db = MySQLdb.connect("localhost","root","123","dict_server")
cursor = db.cursor()
addr = ("192.168.1.3",8088)
sock = socket(AF_INET,SOCK_STREAM)
sock.connect(addr)
while True:
    print "--------1.registe-----------"
    print "--------2.login-------------"
    data = raw_input("command:")
    sock.send(data)
    data = sock.recv(1024)
    #用户注册
    if data == "1":
        data1 = raw_input("name:")
        data2 = raw_input("passwd:")
        sock.send(data1)
        sock.send(data2)
    #用户登录
    elif data == "2":
        data1 = raw_input("name:")
        data2 = raw_input("passwd:")
        sock.send(data1)
        sock.send(data2)
        info = sock.recv(1024)
        print info
        if info[0] == "o":
            #用户登录后操作
            word = ""
            while True:
                print '''
                        -----------------------------------
                        ----1.select--2.history--3.quit----
                        -----------------------------------
                    '''
                data = raw_input("command:")
                sock.send(data)
                data = sock.recv(1024)
                print data
                #获得提示后输入要查询的单词
                if data[:6] == "please":
                    word = raw_input("")
                    sock.send(word)
                    explain = sock.recv(1024)
                    print explain
                if data == "quitttt":
                        break
                elif data == "hhh":
                    sql = "select * from history" 
                    cursor.execute(sql)
                    db.commit()
                    row = cursor.fetchall()
                    for i in row:
                        print
                        for j in i:
                            print j


                        

            
        elif info[0] == "p":
           print info 
           break
        else:
            print "don't know!!"
