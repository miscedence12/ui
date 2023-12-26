import socket
import time
import logging
import json
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from ip_cal import get_ipv4_address
open_flag=0
open_semantic=0
is_running=False
create_data_socket_flag=False
import threading
class Ui_client(QThread):
    # finished = pyqtSignal()
    global open_flag
    global is_running
    global create_data_socket_flag
    def __init__(self) :
        super().__init__()
        self.IP = get_ipv4_address()
        self.SERVER_PORT = 10085
        self.data_json=None
        self.data={"robot":1,"msg_id":3151,"result":0,'open':open_flag} 
        self.create_data_socket_flag=create_data_socket_flag
    def Client_connect(self):
        #  === TCP 客户端程序 client.py ===
        print(f"尝试连接主控{self.IP}:{ self.SERVER_PORT}")

        BUFLEN = 1024
        ended=False
        # 实例化一个socket对象，指明TCP协议
        try:
            self.dataSocket = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
            self.create_data_socket_flag=True
            print("创建套接字成功")
        except socket.error as e:
            print("创建套接字失败")
            self.create_data_socket_flag=False
        while not ended:
            try:
                # 连接服务端socket
                self.dataSocket.connect((self.IP, self.SERVER_PORT))
                print("连接主控成功")
                break
            except:
                logging.warning('未发现服务器程序,两秒后尝试继续连接')
                
                time.sleep(2)
       


    def Send_data(self,BUFLEN,send_data):
        
        # 从终端读入用户输入的字符串
        toSend = send_data
        # 发送消息，也要编码为 bytes
        try:
            self.dataSocket.send(toSend.encode("utf8"))
        except BrokenPipeError as e:
            print("主控断开了连接")

        # 等待接收服务端的消息
        #非阻塞模式
        self.dataSocket.setblocking(0)
        try:
            self.recved = self.dataSocket.recv(BUFLEN)
            
            # 打印读取的信息
            # if self.recved and len(self.recved) not in [212,322,267]:
                # print(self.recved.decode())
            try:
                self.data_json = json.loads(self.recved,encoding="utf-8")  
            except json.decoder.JSONDecodeError as e:
                print(len(self.recved))
                # print("UI_client解析出错:",self.recved.decode())
                print("UI_client解析出错")

            # else:
            #     print("self.recved解析出错")
                   
        except BlockingIOError as e:
            #阻塞模式
            self.dataSocket.setblocking(1)
        # 如果返回空bytes，表示对方关闭了连接
    
        # dataSocket.close()
    def default_dump(self,obj):
        """Convert numpy classes to JSON serializable objects."""
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    def open_gesture(self):
        global open_flag
        print("开启")
        open_flag=1
   

    def close_gesture(self):
        global open_flag
        print("关闭")
        open_flag=0
    def close_gesture(self):
        global open_flag
        open_flag=0

    def open_se(self):
        global open_semantic
        print("开启")
        open_semantic=1
    def close_se(self):
        global open_semantic
        open_semantic=0

    def stop(self):
        global is_running
        is_running=True
    def close_connect(self):
        global is_running
        is_running=True
        if self.create_data_socket_flag:
            self.dataSocket.close()
            print("关闭套接字")


    def run(self):
        global is_running
        is_running=False
        self.Client_connect()
        print("子线程开启")
        while not is_running:
            time.sleep(1)
            # print("发送开启")
            # print(open_flag)
            self.data={"robot":1,"msg_id":3151,"result":0,'open':open_flag,'open_semantic':open_semantic} 
            if self.dataSocket.fileno()!=-1:
                
                self.Send_data(1024,json.dumps(self.data,ensure_ascii=False,default=self.default_dump))
            else:
                self.dataSocket.close()
                self.create_data_socket_flag=False
                print("子控关闭连接")
           

if __name__ =="__main__":
    # client=Ui_client()
    # client.run()
    a={"server_ip": "192.168.227.84", "server_port": 10085, "gesture_ip": "192.168.227.84", "gesture_port": 43004, "zikong_ip": "192.168.227.84", "zikong_port": 43012}
    print(len(a))
