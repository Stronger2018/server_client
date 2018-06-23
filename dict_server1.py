#!/usr/bin/python
#coding=utf-8

from socket import *
import time,sys
from time import strftime
import select
import MySQLdb
import threading 

class Dict_ser():
    def main(self):
        global fd_dict
        global fd
        global db
        global cursor
        global result
        db = MySQLdb.connect("localhost","root","123","dict_server")
        cursor = db.cursor()
        addr = ("192.168.1.3",8088)
        sock = socket(AF_INET,SOCK_STREAM)
        sock.bind(addr)
        sock.listen(5)
        
        fd_dict = {sock.fileno():sock}
        p = select.poll()
        p.register(sock)

        while True:
            conn,addr = sock.accept()
            print "connect from {}".format(addr)
            p.register(conn,select.POLLIN)
            fd_dict[conn.fileno()] = conn
            result = p.poll()
            for fd,events in result:
                if fd_dict[fd] is not sock:
                    if events & select.POLLIN:
                        while True:
                            data = fd_dict[fd].recv(1024)
                            if not data:
                                break
                            if data == "1":
                                self.registe()
                            elif data == "2":
                                self.login()
                            else:
                                print "command error!!"

    #用户注册
    def registe(self):
        fd_dict[fd].send("1")
        data1 = fd_dict[fd].recv(1024)
        data2 = fd_dict[fd].recv(1024)
        try:
            sql = "insert into dict(name,passwd) values('{}','{}')".format(data1,data2)
            print sql
            cursor.execute(sql)
            db.commit()
        except:
            print "this name is already used!"
    #用户登录    
    def login(self):
        global name
        fd_dict[fd].send("2")
        data1 = fd_dict[fd].recv(1024)
        data2 = fd_dict[fd].recv(1024)
        try:
            cursor.execute("select passwd from dict where name = '{}'".format(data1))
            db.commit()
        except:
            fd_dict[fd].send("this name is not exist!!")

        row = cursor.fetchone()    
        #用户登录后的操作
        if data2 in row:
            name = data1
            fd_dict[fd].send("ok")
            self.connect()
        else:
            fd_dict[fd].send("password error!")

    def connect(self):
        while True:
            data = fd_dict[fd].recv(1024)
            if data == "1":
                self.select()
            elif data == "2":
                self.history()
            elif data == "3":
                self.quit()
            else:
                print "command error!!!"

    #查询操作
    def select(self):                                        
        fd_dict[fd].send("please input the word:")
        word = fd_dict[fd].recv(1024)
        length = len(word)
        f = open("/home/linux/net/dict.txt",'r') 
        data = ""
        while str(data[:length]) != word:
            data = f.readline()
            if not data:
                fd_dict[fd].send("this word not exist!!")
        data = f.readline()
        explaining = data[17:]
        fd_dict[fd].send(explaining)
        time1 = strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
        time1 = str(time1)
        print time1
        sql = "insert into history(word,explaining,time,name) values('{}','{}','{}','{}')".format(word,explaining,time1,name)
        try:
            cursor.execute(sql)
            print "insert one set"
        except:
            print "this set is already exist!!"

    #查询历史记录
    def history(self):
        fd_dict[fd].send("hhh")
    
    def quit(self):
        fd_dict[fd].send("quitttt")
        self.main()
        

#   def threadstart(self):
#       threads1 = threading.Thread(target=self.main,args=("192.168.1.6",8088))
#       threads1.start()
#       threads1.join()
#       threads2 = [threading.Thread(target=self.registe,args=(self,)),threading.Thread(target=self.login,args=(self,))]
#       threads2[thread1.start()].start()
#       threads2[].join()
#	threads3 = threading.Thread(target=self.connect,args=(self,))
#       threads4 = [threading.Thread(target=self.select,args=(self,)),threading.Thread(target=self.history,args=(self,))]
#       
#       threads1




if __name__ == "__main__":
    d = Dict_ser()
    d.main()
#    d.threadstart()
