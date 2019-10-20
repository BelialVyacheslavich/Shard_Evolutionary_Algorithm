# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(280, 200)
        MainWindow.setMinimumSize(QtCore.QSize(280, 200))
        MainWindow.setMaximumSize(QtCore.QSize(280, 200))
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vars_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.vars_spin.setGeometry(QtCore.QRect(130, 20, 111, 22))
        self.vars_spin.setMinimum(2)
        self.vars_spin.setMaximum(10)
        self.vars_spin.setObjectName("vars_spin")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.label.setObjectName("label")
        self.calc_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.calc_spin.setGeometry(QtCore.QRect(130, 50, 111, 22))
        self.calc_spin.setMinimum(10000)
        self.calc_spin.setMaximum(1000000000)
        self.calc_spin.setSingleStep(10000)
        self.calc_spin.setObjectName("calc_spin")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 111, 16))
        self.label_2.setObjectName("label_2")
        self.runs_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.runs_spin.setGeometry(QtCore.QRect(130, 80, 111, 22))
        self.runs_spin.setMinimum(1)
        self.runs_spin.setMaximum(999)
        self.runs_spin.setObjectName("runs_spin")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 120, 121, 51))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Input Window"))
        self.label.setText(_translate("MainWindow", "Variables count"))
        self.label_2.setText(_translate("MainWindow", "Calculations count"))
        self.label_3.setText(_translate("MainWindow", "Runs count"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
