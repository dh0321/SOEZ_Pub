# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts")
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts/ui_py_file")
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts/login")
sys.path.insert(0, "/home/rapa/maya/scripts/ez_pub/scripts/maya")

from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit
from PySide2.QtGui import QImage, QPixmap
from login_ui import Ui_MainWindow
from login_model import LogIn
from logger import Logger
from MayaController import MainWindow
import webbrowser


class LoginWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()


    # UI
        self.setupUi(self)
        self.setWindowTitle("KITSU LOGIN")
        self.label_login_error.setText("")
        self.lineEdit_login_pw.setEchoMode(QLineEdit.Password)
        self.img_kitsu = QImage('/home/rapa/maya/scripts/ez_pub/scripts/image/kitsu.png')
        self.label_title_kitsu.setPixmap(QPixmap.fromImage(self.img_kitsu))

        self.label_title_l.clear()
        self.label_title_r.clear()

    # module
        self.log = Logger()
        self.login = LogIn()
        self.mainwindow = MainWindow()

        self.user_dict = self.login.load_login_info()
        if self.user_dict["valid_user"] is True and self.user_dict["auto_login"] is True:
            self.mainwindow.show()
            self.hide()
            self.mainwindow.label_user_name.setText(self.user_dict["user_id"])
        else:
            self.show()

    # signal & slot
        self.pushButton_login.clicked.connect(self.pushButton_login_clicked)
        self.lineEdit_login_email.returnPressed.connect(self.pushButton_login_clicked)
        self.lineEdit_login_pw.returnPressed.connect(self.pushButton_login_clicked)
        self.commandLinkButton_find_pw.clicked.connect(self.find_pw_clicked)

        self.mainwindow.pushButton_logout.clicked.connect(self.logout_clicked)

    def logout_clicked(self):
        self.login.log_out()
        self.mainwindow.close()
        self.show()

    def pushButton_login_clicked(self):

        self.login.host = 'http://192.168.3.117/api'
        self.login.connect_host()

        self.login.user_id = self.lineEdit_login_email.text()
        self.login.user_pw = self.lineEdit_login_pw.text()
        self.login.auto_login_setting = self.checkBox_autologin.isChecked()

        self.login.log_in()
        if self.login.valid_user is True:
            print("성공")
            if self.login.auto_login_setting == True:
                self.login.save_login_info()
                print('자동로그인 정보저장')
            self.window().close()
            self.mainwindow.show()
            self.mainwindow.label_user_name.setText(self.login.user_id)

        else:
            self.set_text_errormassage()
            self.lineEdit_login_pw.clear()

    def set_text_errormassage(self):
        self.label_login_error.setText(self.login.errormassage)
        print("Login label changed!")

    def find_pw_clicked(self):
        forgot_password_browser = 'http://192.168.3.117/reset-password'
        webbrowser.open(forgot_password_browser)


if __name__ == "__main__":

        try:
            LoginWindow.close()
            LoginWindow.deleteLater()
        except:
            pass

        td = LoginWindow()
        td.show()

