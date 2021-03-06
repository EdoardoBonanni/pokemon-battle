from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    # UI used for select the game mode to start a battle.
    def setupUi(self, MainWindow, x, y):
        # GameModeSelection MainWindow and its properties.
        MainWindow.setObjectName("Pokémon Battle Simulator")
        MainWindow.resize(1300, 910)
        MainWindow.setMinimumSize(1300, 910)
        MainWindow.setMaximumSize(1300, 910)
        MainWindow.setGeometry(x, y, 1300, 910)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon_mainwindow = QtGui.QIcon("img/logo.png")
        MainWindow.setWindowIcon(icon_mainwindow)
        MainWindow.setStyleSheet('border-image: url(img/bg_start_battle.png); border-repeat: no-repeat;')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("border-image: None")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(1000, 0))
        self.widget.setMaximumSize(QtCore.QSize(1000, 200))
        self.widget.setStyleSheet("border-image: None")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.title.setStyleSheet("border-image: None")
        self.horizontalLayout.addWidget(self.title)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        # Used for choose a nickname in the game.
        self.insert_name = QtWidgets.QLineEdit(self.widget)
        self.insert_name.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.insert_name.setFont(font)
        self.insert_name.setObjectName("insert_name")
        self.insert_name.setStyleSheet("border-image: None")
        self.horizontalLayout.addWidget(self.insert_name)
        self.verticalLayout.addWidget(self.widget, 0, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.singleplayer = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleplayer.sizePolicy().hasHeightForWidth())

        # Single-player button.
        self.singleplayer.setSizePolicy(sizePolicy)
        self.singleplayer.setMinimumSize(QtCore.QSize(250, 75))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.singleplayer.setFont(font)
        self.singleplayer.setStyleSheet("border-image: None; background-color: #0052cc; color:#ffffff;")
        self.singleplayer.setObjectName("singleplayer")
        self.verticalLayout.addWidget(self.singleplayer, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.multiplayer = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.multiplayer.sizePolicy().hasHeightForWidth())

        # Multi-player button.
        self.multiplayer.setSizePolicy(sizePolicy)
        self.multiplayer.setMinimumSize(QtCore.QSize(250, 75))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.multiplayer.setFont(font)
        self.multiplayer.setStyleSheet("border-image: None; background-color: #2eb82e; color:#ffffff;")
        self.multiplayer.setObjectName("multiplayer")
        self.verticalLayout.addWidget(self.multiplayer, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Exit button to return in ChoosePokemon window.
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit.sizePolicy().hasHeightForWidth())
        self.exit.setSizePolicy(sizePolicy)
        self.exit.setMinimumSize(QtCore.QSize(250, 75))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.exit.setFont(font)
        self.exit.setStyleSheet("border-image: None; background-color: #991f00; color:#ffffff;")
        self.exit.setObjectName("exit")
        self.verticalLayout.addWidget(self.exit, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("border-image: None")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pokémon Battle Simulator"))
        self.title.setText(_translate("MainWindow", "Select a nickname to start the game"))
        self.singleplayer.setText(_translate("MainWindow", "Single-Player"))
        self.multiplayer.setText(_translate("MainWindow", "Multi-Player"))
        self.exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
