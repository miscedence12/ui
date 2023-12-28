from PyQt5.QtWidgets import QApplication,QDialog,QLineEdit,QPushButton,QVBoxLayout,QWidget,QHBoxLayout


class my_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输入框")
        self.input_edit=QLineEdit()
        self.qpushbutton_ok=QPushButton("确定")
        self.qpushbutton_cancel=QPushButton("取消")
        self.qpushbutton_ok.clicked.connect(self.accept)
        self.qpushbutton_cancel.clicked.connect(self.reject)
        layout1=QVBoxLayout()
        layout2=QHBoxLayout()
        layout1.addWidget(self.input_edit)
        layout2.addWidget(self.qpushbutton_cancel)
        layout2.addWidget(self.qpushbutton_ok)
        layout1.addLayout(layout2)

        self.setLayout(layout1)

class my_dialog_delete(QDialog):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("是否确定？")
        self.input_edit=QLineEdit()
        self.input_edit.setStyleSheet('border:none;color:red;')
        self.input_edit.setText("\n是否确定删除数据库?")
        self.qpushbutton_ok=QPushButton("确定")
        self.qpushbutton_cancel=QPushButton("取消")
        self.qpushbutton_ok.clicked.connect(self.accept)
        self.qpushbutton_cancel.clicked.connect(self.reject)
        layout1=QVBoxLayout()
        layout2=QHBoxLayout()
        layout1.addWidget(self.input_edit)
        layout2.addWidget(self.qpushbutton_cancel)
        layout2.addWidget(self.qpushbutton_ok)
        layout1.addLayout(layout2)

        self.setLayout(layout1)

if __name__=="__main__":
    app=QApplication([])
    _my_dialog=my_dialog_delete()
    _my_dialog.show()
    app.exec_()