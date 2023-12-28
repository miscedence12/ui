import sys
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow,QSplashScreen,QProgressBar,QVBoxLayout,QHBoxLayout,QTableWidgetItem,QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt, QTime, QDate
from PyQt5.QtGui import QImage,QPixmap,QIcon,QFont
from ui_client import Ui_client
import signal
from PyQt5 import QtCore
from geometry_msgs.msg import Twist
import subprocess
from painter import Dashboard
import math
from sql_connect import sql_connect
from datetime import datetime
import threading
from dialog import my_dialog,my_dialog_delete
from io import StringIO
import sys
import warnings
import os

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/home/jie/.local/lib/python3.8/site-packages/cv2/qt/plugins/platforms/'
warnings.filterwarnings('ignore',category=DeprecationWarning)
#全局变量
isExit=False
last_linear_vel=0
last_angular_vel=0


class MainWindow(QMainWindow):
    def __init__(self,splash):
        super().__init__()
        self.splash=splash
        QTimer.singleShot(3500,self.init_ui)
      
    ###处理键盘节点控制
    def hand_move(self):
        if self.ui.pushButton_I.isChecked():
            vel_msg.linear.x=0.2
            vel_msg.angular.z=0
        if self.ui.pushButton_point.isChecked():
            vel_msg.linear.x=-0.2
            vel_msg.angular.z=0
        if self.ui.pushButton_point.isChecked():
            vel_msg.linear.x=-0.2
            vel_msg.angular.z=0
        if self.ui.pushButton_J.isChecked():
            vel_msg.linear.x=0
            vel_msg.angular.z=0.2
        if self.ui.pushButton_L.isChecked():
            vel_msg.linear.x=0
            vel_msg.angular.z=-0.2
        if self.ui.pushButton_K.isChecked():
            vel_msg.linear.x=0
            vel_msg.angular.z=0
        if self.ui.pushButton_U.isChecked():
            vel_msg.linear.x=0.1
            vel_msg.angular.z=0.1
        if self.ui.pushButton_O.isChecked():
            vel_msg.linear.x=0.1
            vel_msg.angular.z=-0.1
        if self.ui.pushButton_M.isChecked():
            vel_msg.linear.x=-0.1
            vel_msg.angular.z=-0.2
        if self.ui.pushButton_juhao.isChecked():
            vel_msg.linear.x=-0.1
            vel_msg.angular.z=0.2

        self.pub.publish(vel_msg)
        vel_msg.linear.x=0
        vel_msg.angular.z=0
        rate.sleep()

    def start_moving(self):
        self.time_move.start(100)
    def stop_moving(self):
        self.time_move.stop()

        
       
    def init_ui(self):
         # 加载UI文件
        self.ui=loadUi('/home/jie/ui_server/ui/gesture_control.ui', self)                    #加载ui
        self.ui.progressBar_2.setValue(80)               #设置初始电量
        self.connect_database_flag=False
        #sys.stdout=StreamWrapper(self.ui.output_textEdit) ##重定向输出流

        self.zikong=Ui_client()                          #子控实例化
        self.dashboard1=Dashboard()
        self.dashboard2=Dashboard()
        # self.dashboard.setTitle("线速度")
        # self.dashboard1.setValue(55)
        # set_sudu_thread= threading.Thread(target=self.set_shudu)
        # set_sudu_thread.start()

        layout= QHBoxLayout(self.ui.groupBox_16)
        layout.addWidget(self.dashboard1)
        layout.addWidget(self.dashboard2)

        # self.loca_ip=self.zikong.IP
        # self.local_port=self.zikong.SERVER_PORT
        # self.ui.line_edit_local.setText("ip:"+self.loca_ip+" port:"+str(self.local_port))

        self.ui.progressBar_X.setValue(0)
        self.ui.progressBar_Y.setValue(0)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar_3.setValue(0)
        
        timer1 = QTimer(self)
        timer2 = QTimer(self)
        timer1.timeout.connect(self.show_time)
        timer2.timeout.connect(self.reduce_progress_bar)
        timer1.start(1000)                               #每一秒更新一下时间
        timer2.start(60000)                              #每一分钟更新一下电量

        timer3=QTimer(self)
        timer3.timeout.connect(self.set_gesture_ip)     #每两秒更新一下手势客户端的ip和port
        timer3.start(2000)

        timer4=QTimer(self)
        timer4.timeout.connect(self.set_server_ip)      #每两秒更新一下服务器端的ip和port
        timer4.start(2000)

        timer5=QTimer(self)
        timer5.timeout.connect(self.set_zikong_ip)      #每两秒更新一下子控客户端的ip和port
        timer5.start(2000)

        timer8=QTimer(self)
        timer8.timeout.connect(self.set_yuyi_ip)      #每两秒更新一下语义客户端的ip和port
        timer8.start(2000)
        #键盘控制       
        self.time_move=QTimer(self)
        self.time_move.timeout.connect(self.hand_move)

        #按钮显示槽函数
        self.ui.start_server_3.clicked.connect(self.server_button_click)
        self.ui.pushButton.clicked.connect(self.server_button_click)
        self.ui.start_gesture_3.clicked.connect(self.gesture_button_click)
        self.ui.pushButton_4.clicked.connect(self.gesture_button_click)
        self.ui.start_semantic_3.clicked.connect(self.semantic_button_click)
        self.ui.pushButton_2.clicked.connect(self.semantic_button_click)
        self.ui.stop_button.clicked.connect(self.stop_button_func)
        self.ui.pushButton_3.clicked.connect(self.stop_button_func)
        self.ui.zikong_button.clicked.connect(self.zikong_start)
        ##键盘节点槽函数
        self.ui.pushButton_I.pressed.connect(self.start_moving)
        self.ui.pushButton_I.released.connect(self.stop_moving)
        self.ui.pushButton_point.pressed.connect(self.start_moving)
        self.ui.pushButton_point.released.connect(self.stop_moving)
        self.ui.pushButton_J.pressed.connect(self.start_moving)
        self.ui.pushButton_J.released.connect(self.stop_moving)
        self.ui.pushButton_L.pressed.connect(self.start_moving)
        self.ui.pushButton_L.released.connect(self.stop_moving)
        self.ui.pushButton_U.pressed.connect(self.start_moving)
        self.ui.pushButton_U.released.connect(self.stop_moving)
        self.ui.pushButton_O.pressed.connect(self.start_moving)
        self.ui.pushButton_O.released.connect(self.stop_moving)
        self.ui.pushButton_M.pressed.connect(self.start_moving)
        self.ui.pushButton_M.released.connect(self.stop_moving)
        self.ui.pushButton_juhao.pressed.connect(self.start_moving)
        self.ui.pushButton_juhao.released.connect(self.stop_moving)

        #启动节点槽函数
        self.ui.radioButton.toggled.connect(self.car_base_launch)
        self.ui.radioButton_7.toggled.connect(self.car_driver_launch)
        self.ui.radioButton_3.toggled.connect(self.keyboard_launch)

        ##数据库槽函数
        self.ui.pushButton_5.clicked.connect(self.pushbutton_connect_sql)
        self.ui.pushButton_20.clicked.connect(self.start_save_cmd_vel_thread)
        self.ui.pushButton_21.clicked.connect(self.stop_save_cmd_vel)
        self.ui.pushButton_6.clicked.connect(self.select_database_button)
        self.ui.pushButton_11.clicked.connect(self.show_database)
        self.ui.pushButton_19.clicked.connect(self.clear_show) 
        self.ui.pushButton_8.clicked.connect(self.select_table_button)
        self.ui.pushButton_10.clicked.connect(self.use_database_button)
        self.ui.pushButton_13.clicked.connect(self.show_table)
        self.ui.pushButton_12.clicked.connect(self.select_table)
        self.ui.pushButton_14.clicked.connect(self.delete_database_ok)
        self.ui.pushButton_7.clicked.connect(self.create_database_button)
        self.ui.pushButton_9.clicked.connect(self.create_table_button)
        self.ui.pushButton_sql_exec.clicked.connect(self.exec_sql)
        self.ui.pushButton_sql_input.clicked.connect(self.sql_input)
        self.ui.pushButton_15.clicked.connect(self.clear_output_textEdit)

        # 订阅ROS话题
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/clound_platform/camera/origin_color', Image, self.update_image,queue_size=10)#接收机器人视野图像
        self.image_gesture=rospy.Subscriber("/clound_platform/camera/color", Image, self.update_oak_image,queue_size=10)   #接收手势客户端的图像
        self.speed_sub=rospy.Subscriber("/cmd_vel",Twist,self.update_speed,queue_size=10)
        self.semantic_image_sub=rospy.Subscriber("/camera/semantic/image",Image,self.update_semantic_image,queue_size=10)#接收语义客户端的图像
        self.pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)#创建一个发布者，向话题发布消息

        timer6=QTimer(self)
        timer6.timeout.connect(self.check_robot_shutdown)      #每1秒检查机器人图像发布节点是否被杀死
        timer6.start(1000)

        timer7=QTimer(self)
        timer7.timeout.connect(self.check_gesture_shutdown)      #每1秒检查机器人图像发布节点是否被杀死
        timer7.start(2000)
        #界面展示
        self.show()
     
    #获取当前系统的时间和日期
    def show_time(self):                  
        dateTime = QTime.currentTime()
        date = QDate.currentDate()
        text = "系统时间："+date.toString(Qt.ISODate) + ' ' + dateTime.toString('hh:mm:ss')
        self.ui.label_time_2.setText(text)
    
    #每一分钟减小百分之一的电量
    def reduce_progress_bar(self):
        value = self.ui.progressBar_2.value() - 0.01
        if value < 0:
            value = 0
        self.ui.progressBar_2.setValue(int(value))
     

    #主控制器的启动和关闭
    def server_button_click(self):
        if self.ui.start_server_3.text()=="启动主控制器" or self.ui.pushButton.text()=="启动主控制器":
            self.ui.start_server_3.setText("关闭主控制器")
            self.ui.pushButton.setText("关闭主控制器")
            self.ui.start_server_3.setStyleSheet("color:red")
            self.ui.pushButton.setStyleSheet("color:red")
            self.server_start()
            print("主控启动")
        elif self.ui.start_server_3.text() =="关闭主控制器" or self.ui.pushButton.text()=="关闭主控制器":
            self.ui.start_server_3.setText("启动主控制器")
            self.ui.pushButton.setText("启动主控制器")
            self.ui.start_server_3.setStyleSheet("color:black")
            self.ui.pushButton.setStyleSheet("color:black")
            self.server_close()
            print("主控关闭")
    def server_start(self):
        subprocess.call(["sh", "/home/jie/ui_server/server/server.sh"])
    def server_close(self):
        subprocess.call(["sh", "/home/jie/ui_server/server/server_close.sh"])
    def car_base_launch(self):
        if  self.ui.radioButton.isChecked():
            subprocess.call(["sh", "/home/jie/catkin_new/car_base_launch.sh"])
        else:
            subprocess.call(["sh", "/home/jie/catkin_new/car_base_close.sh"])
    def car_driver_launch(self):
        if  self.ui.radioButton_7.isChecked():
            subprocess.call(["sh", "/home/jie/catkin_new/car_driver.sh"])
        else:
            subprocess.call(["sh", "/home/jie/catkin_new/car_driver_close.sh"])
    def keyboard_launch(self):
        if  self.ui.radioButton_3.isChecked():
            subprocess.call(["sh", "/home/jie/catkin_new/keyboard_launch.sh"])
        else:
            subprocess.call(["sh", "/home/jie/catkin_new/keyboard_close.sh"])


    #手势客户端的启动和关闭
    def gesture_button_click(self):
        if self.ui.start_gesture_3.text()=="启动手势客户端" or self.ui.pushButton_4.text()=="启动手势客户端":
            self.zikong.open_gesture()
            self.ui.start_gesture_3.setText("关闭手势客户端")
            self.ui.pushButton_4.setText("关闭手势客户端")
            self.ui.start_gesture_3.setStyleSheet("color:red")
            self.ui.pushButton_4.setStyleSheet("color:red")
        elif self.ui.start_gesture_3.text() =="关闭手势客户端" or self.ui.pushButton_4.text()=="关闭手势客户端":
            self.zikong.close_gesture()
            self.ui.start_gesture_3.setText("启动手势客户端")
            self.ui.pushButton_4.setText("启动手势客户端")
            self.ui.start_gesture_3.setStyleSheet("color:black")
            self.ui.pushButton_4.setStyleSheet("color:black")

    #语义客户端的启动和关闭
    def semantic_button_click(self):
        if self.ui.start_semantic_3.text()=="启动语义客户端" or self.ui.pushButton_2.text()=="启动语义客户端":
            self.zikong.open_se()
            self.ui.start_semantic_3.setText("关闭语义客户端")
            self.ui.pushButton_2.setText("关闭语义客户端")
            self.ui.start_semantic_3.setStyleSheet("color:red")
            self.ui.pushButton_2.setStyleSheet("color:red")
        elif self.ui.start_semantic_3.text() =="关闭语义客户端" or self.ui.pushButton_2.text()=="关闭语义客户端":
            self.zikong.close_se()
            self.ui.start_semantic_3.setText("启动语义客户端")
            self.ui.pushButton_2.setText("启动语义客户端")
            self.ui.start_semantic_3.setStyleSheet("color:black")
            self.ui.pushButton_2.setStyleSheet("color:black")

    #紧急停止功能的实现
    def stop_button_func(self):
        if self.ui.stop_button.text()=="紧急停止" or self.ui.pushButton_3.text()=="紧急停止":
            self.ui.stop_button.setText("已停止")
            self.ui.pushButton_3.setText("已停止")
            self.ui.stop_button.setStyleSheet("color:red")
            self.ui.pushButton_3.setStyleSheet("color:red")
        elif self.ui.stop_button.text()=="已停止" or self.ui.pushButton_3.text()=="已停止":
            self.ui.stop_button.setText("紧急停止")
            self.ui.pushButton_3.setText("紧急停止")
            self.ui.stop_button.setStyleSheet("color:black")
            self.ui.pushButton_3.setStyleSheet("color:black")

    #子控的开启和关闭实现
    def zikong_start(self):
        if self.ui.start_server_3.text()=="关闭主控制器":
            if  self.ui.zikong_button.text()=="启动子控":
                self.zikong.start()
                self.ui.zikong_button.setText("关闭子控")
                self.ui.zikong_button.setStyleSheet("color:red")
            elif self.ui.zikong_button.text()=="关闭子控":
                self.ui.zikong_button.setStyleSheet("color:black")
                self.zikong.close_connect()
                self.ui.zikong_button.setText("启动子控") 
        else:
            print("主控没有启动，请先启动主控")

    #显示手势客户端的ip和port
    def set_gesture_ip(self):
        if self.zikong.data_json:
            if 'gesture_ip' in self.zikong.data_json:
                self.gesture_ip=self.zikong.data_json['gesture_ip']
                self.gesture_port=self.zikong.data_json['gesture_port']
                self.ui.line_edit_geature.setText("ip:"+self.gesture_ip+" port:"+str(self.gesture_port))

    #显示服务器的ip和port
    def set_server_ip(self):
        if self.zikong.data_json:
            if 'server_ip' in self.zikong.data_json:
                self.server_ip=self.zikong.data_json['server_ip']
                self.server_port=self.zikong.data_json['server_port']
                self.ui.line_edit_server.setText("ip:"+self.server_ip+" port:"+str(self.server_port))
            else:
                self.ui.line_edit_server.clear()
        else:
            self.ui.line_edit_server.clear()

    #显示子控端的ip和port
    def set_zikong_ip(self):
        if self.zikong.data_json:
            if 'zikong_ip' in self.zikong.data_json:
                self.zikong_ip=self.zikong.data_json['zikong_ip']
                self.zikong_port=self.zikong.data_json['zikong_port']

                self.ui.line_edit_local.setText("ip:"+self.zikong_ip+" port:"+str(self.zikong_port))
            else:
                self.ui.line_edit_local.clear()
        else:
            self.ui.line_edit_local.clear()
    #显示语义端的ip和port
    def set_yuyi_ip(self):
        if self.zikong.data_json:
            if 'yuyi_ip' in self.zikong.data_json:
                self.yuyi_ip=self.zikong.data_json['yuyi_ip']
                self.yuyi_port=self.zikong.data_json['yuyi_port']

                self.ui.line_edit_semantic.setText("ip:"+self.yuyi_ip+" port:"+str(self.yuyi_port))
            else:
                self.ui.line_edit_semantic.clear()
        else:
            self.ui.line_edit_semantic.clear()

    def update_image(self, data):
        # 将ROS消息转换为OpenCV图像
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        # 将OpenCV图像转换为QImage
        height, width, channel = cv_image.shape
        bytesPerLine = 3 * width
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        q_image = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 将QImage显示在QLabel上
        pixmap = QPixmap.fromImage(q_image)
        # self.ui.label2.setPixmap(pixmap)
        # self.ui.label_4.setPixmap(pixmap)
        if self.ui.radioButton_5.isChecked():
            self.ui.label_28.setPixmap(pixmap)
            self.ui.label2.setPixmap(pixmap)
            self.ui.label_4.setPixmap(pixmap)
        else:
            self.ui.label_28.clear()
            self.ui.label2.clear()
            self.ui.label_4.clear()


    def check_robot_shutdown(self):
        if self.image_sub.get_num_connections() == 0:
            self.ui.label_4.clear()  # 如果发布节点已经停止，则清空QLabel的图像
            self.ui.label2.clear()  # 如果发布节点已经停止，则清空QLabel的图像
            self.ui.label_4.setText("机器人视野图像")
            self.ui.label2.setText("机器人视野图像")

    def check_gesture_shutdown(self):
        if self.image_gesture.get_num_connections()==0:
            self.ui.label1.clear()   # 如果手势客户端节点已经停止，则清空QLabel的图像
            self.ui.label1.setText("手势客户端图像")
    def check_semantic_shutdown(self):
        if self.semantic_image_sub.get_num_connections()==0:
            self.ui.label_5.clear()
            self.ui.label_5.setText("语义客户端图像")

    def update_oak_image(self,data):
        if self.ui.start_gesture_3.text() =="关闭手势客户端":
            # 将ROS消息转换为OpenCV图像
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # 将OpenCV图像转换为QImage
            height, width, channel = cv_image.shape
            bytesPerLine = 3 * width
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # 将QImage显示在QLabel上
            pixmap = QPixmap.fromImage(q_image)
            self.ui.label1.setPixmap(pixmap)
        else:
            self.ui.label1.clear()
            self.ui.label1.setText("手势客户端图像")
    def update_speed(self,data):
        global last_linear_vel
        global last_angular_vel

        linear_vel=data.linear.x
        angular_vel=data.angular.z
        self.ui.progressBar_X.setValue(int(linear_vel*10))
        self.ui.progressBar_Y.setValue(int(angular_vel*10))
        self.ui.progressBar.setValue(int(linear_vel*10))
        self.ui.progressBar_3.setValue(int(angular_vel*10))
        result_vel=np.linspace(last_linear_vel,linear_vel,10)
        result_angular=np.linspace(last_angular_vel,angular_vel,10)
      
        if last_linear_vel != linear_vel:
            for i in result_vel:
                self.dashboard1.updateSpeed(int(i*100))
                time.sleep(0.08)
                # self.dashboard2.updateSpeed(int(angular_vel*100))
        if last_angular_vel !=angular_vel:
            for i in result_angular:
                self.dashboard2.updateSpeed(int(i*180/math.pi))
                time.sleep(0.08)

        if self.speed_sub.get_num_connections()==0:
            self.ui.progressBar_X.setValue(0)
            self.ui.progressBar_Y.setValue(0)
            self.ui.progressBar.setValue(0)
            self.ui.progressBar_3.setValue(0)
        last_angular_vel=angular_vel
        last_linear_vel=linear_vel


    def update_semantic_image(self,data):
        # 将ROS消息转换为OpenCV图像
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image=cv2.resize(cv_image,(640,480))
        # 将OpenCV图像转换为QImage
        height, width, channel = cv_image.shape
        bytesPerLine = 3 * width
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        q_image = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # 将QImage显示在QLabel上
        pixmap = QPixmap.fromImage(q_image)
        self.ui.label_5.setPixmap(pixmap)

    def closeEvent(self, event):
        # 在窗口关闭时停止Worker对象
        self.zikong.stop()
        self.zikong.wait()
        super().closeEvent(event)

    def load_data(self):
        for i in range(1, 11):     #模拟主程序加载过程
            time.sleep(0.3)        #加载数据
            self.splash.showMessage("初始化中... {}%          版本号:V1.0".format(int(i * 10)), QtCore.Qt.AlignHCenter |QtCore.Qt.AlignBottom, QtCore.Qt.black)
    
  


    #####数据库部分
    def pushbutton_connect_sql(self):
        if self.ui.pushButton_5.text()=="打开数据库连接":
            sql_driver=self.ui.lineEdit.text()
            hostname=self.ui.lineEdit_2.text()
            port=self.ui.lineEdit_3.text()
            username=self.ui.lineEdit_4.text()
            password=self.ui.lineEdit_5.text()
            self.db,self.query=sql_connect(sql_driver,hostname,username,password,port)
            if self.db:
                self.connect_database_flag=True
           
            self.ui.pushButton_5.setText("关闭数据库连接")
            self.ui.pushButton_5.setStyleSheet("color:red")

        elif self.ui.pushButton_5.text()=="关闭数据库连接":
            self.ui.pushButton_5.setText("打开数据库连接")
            self.ui.pushButton_5.setStyleSheet("color:black")
            self.db.close()
            self.query.clear()
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

            if self.db.isOpen():
                print("数据库关闭失败，请重新尝试")
            else:
                print("数据库关闭成功")
                self.connect_database_flag=False
    def save_cmd_vel(self):
        global isExit
        if self.ui.pushButton_20.text()=="保存小车状态":
            ("开启保存状态成功")
       
            self.ui.pushButton_20.setStyleSheet("color:red")
            self.ui.pushButton_20.setText("保存状态开启")
            while not isExit:
                time.sleep(1)
                current_time=datetime.now()
                current_time=current_time.strftime("%Y-%m-%d %H:%M:%S")
                cmd_vel_msg=rospy.wait_for_message('/scout_base_controller/cmd_vel',Twist)
                
                linear_x=float(cmd_vel_msg.linear.x)
                angular_z=float(cmd_vel_msg.angular.z)
                print(current_time,linear_x,angular_z)
                self.query.prepare("INSERT INTO cmd_vel1 (timestamp,linear_x,angular_z) values(:value1,:value2,:value3)")
                self.query.bindValue(":value1",current_time)
                self.query.bindValue(":value2",linear_x)
                self.query.bindValue(":value3",angular_z)
                if self.query.exec():
                    print("插入数据成功")
                else:
                    print("插入数据失败",self.query.lastError().text())
    def start_save_cmd_vel_thread(self):
        if self.ui.radioButton.isChecked():
            cmd_vel_thread=threading.Thread(target=self.save_cmd_vel)
            cmd_vel_thread.start()
        else:
            print("小车底盘节点未启动，请先启动底盘节点")
    def stop_save_cmd_vel(self):
        if self.ui.radioButton.isChecked():
            global isExit
            isExit=True
            print("取消保存状态成功")
            self.ui.pushButton_20.setStyleSheet("color:black")
            self.ui.pushButton_20.setText("保存小车状态")
        else:
            print("小车底盘节点未启动，请先启动底盘节点")
    def select_database_button(self):
        if self.connect_database_flag:
            dialog=my_dialog()
            dialog.setModal(True)
            if dialog.exec_()==QDialog.Accepted:
                self.dialog_text=dialog.input_edit.text()
                print("选择的数据库为：",self.dialog_text)
            else:
                print("取消选择")
        else:
            print("数据库未正常连接，请先连接数据库")
    def show_on_tableWidget(self):
        # #设置表格的行数和列数
        row_count=self.query.size()
        column_count=self.query.record().count()
        self.ui.tableWidget.setRowCount(row_count)
        self.ui.tableWidget.setColumnCount(column_count)
        # 显示在tablewidget上
        row=0
        while self. query.next():
            for colum in range(column_count):
                value=self.query.value(colum)
                item=QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row,colum,item)
            row+=1
    def show_database(self):
        if self.connect_database_flag :
            self.query.exec('show databases')
            self.show_on_tableWidget()
        
        else:
            print("输入无效")
    def use_database_button(self):
        if self.connect_database_flag:
            try:
                self.determin_database_isExit(self.dialog_text)
                if self.database_isExit:
                    self.query.exec('use {}'.format(self.dialog_text))
                    print("database changes")
                else:
                    print("输入的数据库不存在，请重新输入")
            except:
                print("未选择数据库")
        else:
            print("数据库未正常连接，请先连接数据库")

    def select_table_button(self):
        if self.connect_database_flag:
            dialog1=my_dialog()
            dialog1.setModal(True)
            if dialog1.exec_()==QDialog.Accepted:
                self.dialog_text1=dialog1.input_edit.text()
                print("选择的表为：",self.dialog_text1)
            else:
                print("取消选择")
        else:
            print("数据库未正常连接，请先连接数据库")
    def show_table(self):
        if self.connect_database_flag:
            self.query.exec('show tables')
            self.show_on_tableWidget()
        
        else:
            print("输入无效")
    def select_table(self):
        try:
            if self.connect_database_flag  and  self.dialog_text1:
                self.query.exec('select * from  {}'.format(self.dialog_text1))
                self.show_on_tableWidget()
            else:
                print("输入无效")
        except:
            print("未选择表，请先选择需要查询的表")

    def clear_show(self):
        if self.connect_database_flag:
            self.query.clear()
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)
    def delete_database_ok(self):
        if self.connect_database_flag :
            try:
                if self.dialog_text:
                    my_database_delete_dialog=my_dialog_delete()
                    my_database_delete_dialog.setModal(True)
                    if my_database_delete_dialog.exec_()==QDialog.Accepted:
                        self.dialog_text3=my_database_delete_dialog.input_edit.text()
                        print("选择删除的数据库为：",self.dialog_text3)
                        self.delete_database_button()
                    else:
                        print("取消选择")
            except:
                print("未选择需要删除的数据库，请先选择需要删除的数据库")
        else:
            print("数据库未连接，请先连接数据库")

    def delete_database_button(self):
        if self.connect_database_flag and self.dialog_text and self.dialog_text not in ['information_schema','sys','mysql' ,'performance_schema','cmd_vel']:
            self.determin_database_isExit(self.dialog_text)
            if self.database_isExit:
                self.query.exec('drop database if exists {} '.format(self.dialog_text))
                print("{}数据库被删除成功".format(self.dialog_text))
            else:
                 print("数据库不存在，请重新选择")
            
        elif self.dialog_text and self.dialog_text  in ['information_schema','sys','mysql' ,'performance_schema','cmd_vel']:
            print("错误:{}数据库不允许被删除".format(self.dialog_text ))

    def determin_database_isExit(self,database_name):
        self.query.exec_("show databases")
        self.database_isExit=False
        while self.query.next():
            name=self.query.value(0)
            if name==database_name:
                self.database_isExit=True
                break
            else:
                self.database_isExit=False
    def create_database_button(self):
        if self.connect_database_flag :
            try:
                if self.dialog_text:
                    self.determin_database_isExit(self.dialog_text)
                    if self.database_isExit:
                        print("该数据库已经存在，无法创建，请重新输入")
                    else:
                        print("创建成功")
                        self.query.exec_("create database {}".format(self.dialog_text))
            except:
                print("未选择需要创建的数据库，请先选择需要创建的数据库")
        else:
            print("数据库未连接，请先连接数据库")
    def determin_table_isExit(self,table_name):
        self.query.exec_("show tables")
        self.table_isExit=False
        while self.query.next():
            name=self.query.value(0)
            if name==table_name:
                self.table_isExit=True
                break
            else:
                self.table_isExit=False
    def create_table_button(self):
        if self.connect_database_flag :
            try:
                if self.dialog_text1 and self.dialog_text:
                    self.determin_table_isExit(self.dialog_text1)
                    if self.table_isExit :
                        print("该表已经存在，无法创建，请重新输入")
                    else:
                        print("创建成功")
                        self.query.exec_("create table {}".format(self.dialog_text1))
            except:
                print("未输入需要创建的表,或者未先选择数据库并使用")
        else:
            print("数据库未连接，请先连接数据库")
    
    def exec_sql(self):
        sql_text=self.sql_TextEdit.toPlainText()
        print("输入文本为：",sql_text)
        if not self.query.exec_(sql_text):
            print("执行失败：",self.query.lastError().text())
        if self.query.isActive():
            print("执行成功")
            self.show_on_tableWidget()
        else:
            print("执行失败")
    def sql_input(self):
        if self.connect_database_flag:
            sql_dialog=my_dialog()
            sql_dialog.setModal(True)
            if sql_dialog.exec_()==QDialog.Accepted:
                self.dialog_text_sql=sql_dialog.input_edit.text()
                print("输入的sql语句为:",self.dialog_text_sql)
                if not self.query.exec_(self.dialog_text_sql):
                    print("执行失败：",self.query.lastError().text())
                if self.query.isActive():
                    print("执行成功")
                    self.show_on_tableWidget()
                else:
                    print("执行失败")
            else:
                print("取消选择")
        else:
            print("数据库未正常连接，请先连接数据库")
    def clear_output_textEdit(self):
        self.ui.output_textEdit.clear()

def Exit(signum,data):
    global isExit
    window.close()
    isExit=True
    print("界面退出")
signal.signal(signal.SIGINT,Exit)

class StreamWrapper:
    def __init__(self,text_edit):
        self.text_edit=text_edit
        self.buffer=StringIO() 
    def write(self,text):
        self.buffer.write(text)
        self.text_edit.setPlainText(self.buffer.getvalue())
    def flush(self):
        pass

if __name__ == '__main__':
    print("界面进程pid:",os.getpid())
    rospy.init_node('image_viewer')
    rate=rospy.Rate(10)#10HZ
    vel_msg=Twist() #创建一个Twist类型的消息
    app = QApplication(sys.argv)
    # 加载启动画面图片
    # 缩放图片
    splash = QSplashScreen(QPixmap('/home/jie/ui_server/ui/logo1.png'))
    
    splash.show()
    # 模拟应用程序启动过程
    # 隐藏启动画面，显示主窗口
    font = QFont()
    font.setPointSize(15)  # 设置字体大小为 20
    splash.setFont(font)
    QTimer.singleShot(3000, splash.close)

    window = MainWindow(splash)
    # ##设置背景
    # window.setStyleSheet(style_sheet)
    window.setWindowIcon(QIcon('/home/jie/ui_server/ui/logo.png')) 
    window .load_data()
   
    # window.show()
    app.exec_()
