from PyQt5.QtSql import QSqlDatabase,QSqlQuery

def sql_connect(driver,hostname,username,password,port):
    db = QSqlDatabase.addDatabase(driver)
    db.setHostName(hostname)  # 主机名
    db.setUserName(username)  # 用户名
    db.setPassword(password)  # 密码
    # db.setDatabaseName('cmd_vel')  # 数据库名称
    db.setPort(int(port))
    query = QSqlQuery()
    if db.open():
        print('Connected to MySQL database successfully')
        return db,query
    else:
        print('Failed to connect to MySQL database:', db.lastError().text())
        return 
    # query.exec('SELECT * FROM tb_user')
    # while query.next():
    #     # 获取每一列的值
    #     id = query.value(0)
    #     name = query.value(1)
    #     # 打印每一行的值
    #     print(f"ID: {id}, Name: {name}")
   
