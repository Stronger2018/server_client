#!/usr/bin/python 
#coding=utf-8

from signal import *
from socket import *
from time import *
import sys
import os

def do_register(sockfd,msg):
    name = input("input your user name >>")
    passwd = input("input your user passwd >>")
    msg = 'R %s %s'%(name,passwd) 

    sockfd.send(msg.encode())
    msg = sockfd.recv(128).decode()

    if msg[0:2] == 'OK':
        return 0
    else:
        return -1

def do_login(sockfd,msg):
    name = input("input your user name >>")
    passwd = input("input your user passwd >>")
    msg = 'L %s %s'%(name,passwd) 

    sockfd.send(msg.encode())
    msg = sockfd.recv(128).decode()

    if msg[0:2] == 'OK':
        return name
    else:
        return -1

def do_query(sockfd,msg,name):
    while True:
        word = input("input word >>")
    
        if word == '##':
            return

        msg = 'Q %s %s'%(word,name)

        sockfd.send(msg.encode())
        msg = sockfd.recv(128).decode()

        if msg[0:2] == 'OK':
            msg = sockfd.recv(1024).decode()
            if msg[0:9] == "not found":
                print("not found this word")
                continue
            print(msg)

        else:
            print("fail to query")
            continue

def do_history(sockfd,msg,name):
    msg = 'H %s'%name
    sockfd.send(msg.encode())
    msg = sockfd.recv(128).decode()

    if msg[0:2] == 'OK':
        while True:
            data = sockfd.recv(1024).decode()
            if data == 'over':
                break

            print(data)
    else:
        print("fail to history")
        return -1

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    msg = None

    sockfd = socket()

    sockfd.connect((HOST,PORT))

    def login(name):
        while True:
            print('''
            ==========query commend=========
            ---1:查词  2:历史记录  3:退出---
            ================================
            ''')
            try:
                cmd = int(input("Input commend >> "))
            except:
                print("Input error!")
                continue

            if cmd not in [1,2,3]:
                print("input error!")
                sys.stdin.flush()
                continue
        
            if cmd == 1:
                do_query(sockfd,msg,name)
            if cmd == 2:
                do_history(sockfd,msg,name)
            if cmd == 3:
                break
        return


    while True:
        print('''
        =============Welcome=============
        ----1: 注册  2: 登陆  3: 退出----
        =================================
        ''')
        try:
            cmd = int(input("Input commend >> "))
        except:
            print("Input error")
            continue

        if cmd not in [1,2,3]:
            print("input error!")
            sys.stdin.flush()
            continue
        
        if cmd == 1:
            if do_register(sockfd,msg) == 0:
                print("register OK!")
            else:
                print( "register FALL")
        if cmd == 2:
            name = do_login(sockfd,msg)
            if name != -1:
                print ("login OK!")
                login(name)
            else:
                print ("register FALL")
        if cmd == 3:
            msg = 'E'
            sockfd.send(msg.encode())
            sockfd.close()
            sys.exit(0)

if __name__ == "__main__":
    main()
