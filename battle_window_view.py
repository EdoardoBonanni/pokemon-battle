# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'battle.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pygame

class ImageWidget(QtWidgets.QWidget):
    def __init__(self, surface, parent=None):
        super(ImageWidget,self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        self.label = QtWidgets.QLabel()
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)
        qimg_pixmap = QtGui.QPixmap.fromImage(self.image)
        self.label.setPixmap(qimg_pixmap)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update(self, surface):
        self.data = surface.get_buffer().raw
        self.image = QtGui.QImage(self.data, self.w, self.h, QtGui.QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0, self.image)
        qp.end()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 900))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setMaximumSize(QtCore.QSize(850, 350))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.button_1 = QtWidgets.QPushButton(self.widget_3)
        self.button_1.setMinimumSize(QtCore.QSize(0, 50))
        self.button_1.setObjectName("button_1")
        self.gridLayout_3.addWidget(self.button_1, 0, 0, 1, 1)
        self.button_2 = QtWidgets.QPushButton(self.widget_3)
        self.button_2.setMinimumSize(QtCore.QSize(0, 50))
        self.button_2.setObjectName("button_2")
        self.gridLayout_3.addWidget(self.button_2, 0, 1, 1, 1)
        self.button_3 = QtWidgets.QPushButton(self.widget_3)
        self.button_3.setMinimumSize(QtCore.QSize(0, 50))
        self.button_3.setObjectName("button_3")
        self.gridLayout_3.addWidget(self.button_3, 1, 0, 1, 1)
        self.button_4 = QtWidgets.QPushButton(self.widget_3)
        self.button_4.setMinimumSize(QtCore.QSize(0, 50))
        self.button_4.setObjectName("button_4")
        self.gridLayout_3.addWidget(self.button_4, 1, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 1, 1, 1, 1, QtCore.Qt.AlignVCenter)

        self.widget_choice = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_choice.sizePolicy().hasHeightForWidth())
        self.widget_choice.setSizePolicy(sizePolicy)
        self.widget_choice.setMaximumSize(QtCore.QSize(650, 350))
        self.widget_choice.setObjectName("widget_choice")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_choice)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_text = QtWidgets.QLabel(self.widget_choice)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_text.setFont(font)
        self.label_text.setObjectName("label_text")
        self.verticalLayout.addWidget(self.label_text)
        self.widget_option = QtWidgets.QWidget(self.widget_choice)
        self.widget_option.setObjectName("widget_option")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_option)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_team = QtWidgets.QPushButton(self.widget_option)
        self.button_team.setMinimumSize(QtCore.QSize(0, 50))
        self.button_team.setObjectName("button_team")
        self.horizontalLayout.addWidget(self.button_team, 0, QtCore.Qt.AlignBottom)
        self.button_moves = QtWidgets.QPushButton(self.widget_option)
        self.button_moves.setMinimumSize(QtCore.QSize(50, 50))
        self.button_moves.setObjectName("button_moves")
        self.horizontalLayout.addWidget(self.button_moves, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.widget_option)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout_2.addWidget(self.widget_choice, 1, 0, 1, 1)

        pygame.init()
        s = pygame.Surface([1300,800], pygame.SRCALPHA, 32)
        #background_image = pygame.image.load('img/battle_bg_1.png')
        #s = s.convert_alpha()
        s.set_colorkey((0, 0, 0))
        # s.fill((255,100,192,100))
        pygame.draw.circle(s,(255,255,255,255),(100,100),50)
        self.battlefield = ImageWidget(s, QtWidgets.QWidget(self.centralwidget))
        # self.battlefield = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.battlefield.sizePolicy().hasHeightForWidth())
        self.battlefield.setSizePolicy(sizePolicy)
        self.battlefield.setObjectName("battlefield")
        # self.battlefield.setStyleSheet("border-image: url(img/battle_bg_1.png); border-repeat: no-repeat;")
        # self.gridLayout = QtWidgets.QGridLayout(self.battlefield)
        # self.gridLayout.setObjectName("gridLayout")
        # self.widget_player = QtWidgets.QWidget(self.battlefield)
        # self.widget_player.setObjectName("widget_player")
        # self.gridLayout.addWidget(self.widget_player, 1, 0, 1, 1)
        # #self.gridLayout.addWidget(self.widget_player, 1, 0, 1, 1)
        # self.widget_hp_enemy = QtWidgets.QWidget(self.battlefield)
        # self.widget_hp_enemy.setObjectName("widget_hp_enemy")
        # self.widget_hp_enemy.setStyleSheet("border-image: None;")
        # self.gridLayout.addWidget(self.widget_hp_enemy, 0, 0, 1, 1)
        # self.widget_enemy = QtWidgets.QWidget(self.battlefield)
        # self.widget_enemy.setObjectName("widget_enemy")
        # self.widget_enemy.setStyleSheet("border-image: none;")
        # self.gridLayout.addWidget(self.widget_enemy, 0, 1, 1, 1)
        # self.widget_hp_player = QtWidgets.QWidget(self.battlefield)
        # self.widget_hp_player.setObjectName("widget_hp_player")
        # self.widget_hp_player.setStyleSheet("border-image: transparent;")
        # self.gridLayout.addWidget(self.widget_hp_player, 1, 1, 1, 1)

        # self.gridLayout_2.addWidget(ImageWidget(s, self.battlefield), 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.battlefield, 0, 0, 1, 2)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1012, 26))
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
        self.button_1.setText(_translate("MainWindow", "PushButton"))
        self.button_2.setText(_translate("MainWindow", "PushButton"))
        self.button_3.setText(_translate("MainWindow", "PushButton"))
        self.button_4.setText(_translate("MainWindow", "PushButton"))
        self.label_text.setText(_translate("MainWindow", "Cosa vuoi fare? Fai la tua scelta!"))
        self.button_team.setText(_translate("MainWindow", "Choose Pokemon"))
        self.button_moves.setText(_translate("MainWindow", "Battle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

