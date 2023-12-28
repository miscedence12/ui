<<<<<<< HEAD
## sensor.py是主脚本，可以直接运行这个脚本即可启动手势控制平台的界面。 作者使用的环境为Ubuntu20.04、Python3.8, ros-noetic，pyqt5 5.15.4

1、ROS安装：作者使用鱼香ROS进行安装，其地址链接为[https://fishros.org.cn/forum/topic/20/%E5%B0%8F%E9%B1%BC%E7%9A%84%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E7%B3%BB%E5%88%97?lang=zh-CN。（作者使用的是noetic版本,ubuntu20.04）](https://fishros.org.cn/forum/topic/20/小鱼的一键安装系列?lang=zh-CN。（作者使用的是noetic版本,ubuntu20.04）)



一键安装的脚本如下:

```
wget http://fishros.com/install -O fishros && . fishros
```

请选择noetic完整版

2、Pyqt5安装 可以直接使用pip安装，安装指令如下：

```
pip install PyQt5== 5.15.4 -i https://pypi.douban.com/simple 
pip install PyQt5-tools -i https://pypi.douban.com/simple
```

Note: 作者在装ubuntu20.04的时候发现系统好像自带pyqt5，如果运行报没有 PyQt5的错，就自行进行安装。

3、mysql服务安装

```
sudo apt-get install mysql-server
启动mysql服务：systemctl start mysql-server 
使用脚本连接mysql服务还需要安装pymsql:pip install pymysql -i https://pypi.douban.com/simple 
```

>>>>>>> 
