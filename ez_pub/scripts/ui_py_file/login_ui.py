# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(370, 260)
        MainWindow.setMinimumSize(QSize(370, 260))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.loginLayout_0 = QVBoxLayout()
        self.loginLayout_0.setObjectName(u"loginLayout_0")
        self.loginLayout_1 = QGridLayout()
        self.loginLayout_1.setObjectName(u"loginLayout_1")
        self.label_title_l = QLabel(self.centralwidget)
        self.label_title_l.setObjectName(u"label_title_l")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title_l.sizePolicy().hasHeightForWidth())
        self.label_title_l.setSizePolicy(sizePolicy)
        self.label_title_l.setMinimumSize(QSize(0, 0))
        self.label_title_l.setScaledContents(True)

        self.loginLayout_1.addWidget(self.label_title_l, 0, 0, 1, 1)

        self.label_title_kitsu = QLabel(self.centralwidget)
        self.label_title_kitsu.setObjectName(u"label_title_kitsu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_title_kitsu.sizePolicy().hasHeightForWidth())
        self.label_title_kitsu.setSizePolicy(sizePolicy1)
        self.label_title_kitsu.setMinimumSize(QSize(110, 80))
        self.label_title_kitsu.setScaledContents(True)
        self.label_title_kitsu.setAlignment(Qt.AlignCenter)

        self.loginLayout_1.addWidget(self.label_title_kitsu, 0, 1, 2, 1)

        self.label_title_r = QLabel(self.centralwidget)
        self.label_title_r.setObjectName(u"label_title_r")
        sizePolicy.setHeightForWidth(self.label_title_r.sizePolicy().hasHeightForWidth())
        self.label_title_r.setSizePolicy(sizePolicy)
        self.label_title_r.setMinimumSize(QSize(0, 0))
        self.label_title_r.setScaledContents(True)
        self.label_title_r.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.loginLayout_1.addWidget(self.label_title_r, 0, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(60, 30, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.loginLayout_1.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(60, 30, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.loginLayout_1.addItem(self.verticalSpacer_2, 1, 2, 1, 1)


        self.loginLayout_0.addLayout(self.loginLayout_1)

        self.loginLayout_2 = QGridLayout()
        self.loginLayout_2.setObjectName(u"loginLayout_2")
        self.lineEdit_login_email = QLineEdit(self.centralwidget)
        self.lineEdit_login_email.setObjectName(u"lineEdit_login_email")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_login_email.sizePolicy().hasHeightForWidth())
        self.lineEdit_login_email.setSizePolicy(sizePolicy2)
        self.lineEdit_login_email.setMinimumSize(QSize(0, 30))

        self.loginLayout_2.addWidget(self.lineEdit_login_email, 0, 0, 1, 1)

        self.pushButton_login = QPushButton(self.centralwidget)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy1.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy1)
        self.pushButton_login.setMinimumSize(QSize(0, 0))

        self.loginLayout_2.addWidget(self.pushButton_login, 0, 1, 2, 1)

        self.lineEdit_login_pw = QLineEdit(self.centralwidget)
        self.lineEdit_login_pw.setObjectName(u"lineEdit_login_pw")
        sizePolicy2.setHeightForWidth(self.lineEdit_login_pw.sizePolicy().hasHeightForWidth())
        self.lineEdit_login_pw.setSizePolicy(sizePolicy2)
        self.lineEdit_login_pw.setMinimumSize(QSize(0, 30))

        self.loginLayout_2.addWidget(self.lineEdit_login_pw, 1, 0, 1, 1)

        self.commandLinkButton_find_pw = QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_find_pw.setObjectName(u"commandLinkButton_find_pw")
        self.commandLinkButton_find_pw.setMinimumSize(QSize(0, 0))

        self.loginLayout_2.addWidget(self.commandLinkButton_find_pw, 2, 0, 1, 1)

        self.checkBox_autologin = QCheckBox(self.centralwidget)
        self.checkBox_autologin.setObjectName(u"checkBox_autologin")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBox_autologin.sizePolicy().hasHeightForWidth())
        self.checkBox_autologin.setSizePolicy(sizePolicy3)
        self.checkBox_autologin.setMinimumSize(QSize(0, 0))

        self.loginLayout_2.addWidget(self.checkBox_autologin, 2, 1, 1, 1)

        self.label_login_error = QLabel(self.centralwidget)
        self.label_login_error.setObjectName(u"label_login_error")
        self.label_login_error.setMinimumSize(QSize(0, 0))

        self.loginLayout_2.addWidget(self.label_login_error, 3, 0, 1, 2)


        self.loginLayout_0.addLayout(self.loginLayout_2)


        self.gridLayout_2.addLayout(self.loginLayout_0, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"KITSU LOGIN", None))
        self.label_title_l.setText("")
        self.label_title_kitsu.setText(QCoreApplication.translate("MainWindow", u"KITSU LOGIN", None))
        self.label_title_r.setText("")
        self.lineEdit_login_email.setText("")
        self.lineEdit_login_email.setPlaceholderText(QCoreApplication.translate("MainWindow", u"E-mail", None))
        self.pushButton_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.lineEdit_login_pw.setText("")
        self.lineEdit_login_pw.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.commandLinkButton_find_pw.setText(QCoreApplication.translate("MainWindow", u"Find Password", None))
        self.checkBox_autologin.setText(QCoreApplication.translate("MainWindow", u"Auto Login", None))
        self.label_login_error.setText(QCoreApplication.translate("MainWindow", u"set error message", None))
    # retranslateUi

