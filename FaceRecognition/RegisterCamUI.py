# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RegisterCamUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UI_RegisterCamWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(691, 740)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)

        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 564, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        # self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        # self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Title = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Title.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title)
        self.CameraView = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.CameraView.setMinimumSize(QtCore.QSize(0, 500))
        self.CameraView.setFrameShape(QtWidgets.QFrame.Box)
        self.CameraView.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CameraView.setLineWidth(5)
        self.CameraView.setText("")
        self.CameraView.setObjectName("CameraView")
        self.verticalLayout.addWidget(self.CameraView)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.NameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.NameLabel.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Arial Nova")
        font.setPointSize(14)
        self.NameLabel.setFont(font)
        self.NameLabel.setObjectName("NameLabel")
        self.horizontalLayout_3.addWidget(self.NameLabel)
        self.Name_textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.Name_textEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.Name_textEdit.setMaximumSize(QtCore.QSize(10000, 40))
        self.Name_textEdit.setObjectName("Name_textEdit")
        self.horizontalLayout_3.addWidget(self.Name_textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BackButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.BackButton.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.BackButton.setFont(font)
        self.BackButton.setObjectName("BackButton")
        self.horizontalLayout.addWidget(self.BackButton)
        self.TakeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.TakeButton.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.TakeButton.setFont(font)
        self.TakeButton.setObjectName("TakeButton")
        self.horizontalLayout.addWidget(self.TakeButton)
        self.SaveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.SaveButton.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.SaveButton.setFont(font)
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout.addWidget(self.SaveButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 691, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "Please close to the camera"))
        self.NameLabel.setText(_translate("MainWindow", "Your name"))
        self.Name_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.BackButton.setText(_translate("MainWindow", "Back"))
        self.TakeButton.setText(_translate("MainWindow", "Take!"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_RegisterCamWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())