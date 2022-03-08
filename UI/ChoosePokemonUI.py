from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    # UI used for Pokemon team choice.
    def setupUi(self, MainWindow):
        # ChoosePokemon MainWindow and its properties.
        MainWindow.setObjectName("Pokemon Battle")
        MainWindow.resize(1300, 910)
        MainWindow.setMinimumSize(1300, 910)
        MainWindow.setMaximumSize(1300, 910)
        MainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        MainWindow.setAnimated(True)
        icon_mainwindow = QtGui.QIcon("img/logo.png")
        MainWindow.setWindowIcon(icon_mainwindow)
        MainWindow.setStyleSheet('background-color: rgb(224, 235, 235);')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # List of all available Pokemon.
        self.list_item = QtWidgets.QListWidget(self.centralwidget)
        self.list_item.setMinimumSize(QtCore.QSize(300, 0))
        self.list_item.setMaximumSize(QtCore.QSize(300, 16777215))
        self.list_item.setSpacing(5)
        self.list_item.setTabKeyNavigation(True)
        self.list_item.setObjectName("list_item")
        self.list_item.setMovement(QtWidgets.QListWidget.Static)
        self.list_item.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.list_item.setViewMode(QtWidgets.QListWidget.ListMode)
        self.list_item.setStyleSheet('background-color: None;')
        self.gridLayout.addWidget(self.list_item, 0, 0, 3, 1)

        # Game logo image at startup;
        # After Pokemon image selected in the list.
        self.pokemon_img = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pokemon_img.sizePolicy().hasHeightForWidth())
        self.pokemon_img.setSizePolicy(sizePolicy)
        self.pokemon_img.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.pokemon_img.setAcceptDrops(True)
        self.pokemon_img.setAutoFillBackground(False)
        self.pokemon_img.setText("")
        self.pokemon_img.setScaledContents(False)
        self.pokemon_img.setAlignment(QtCore.Qt.AlignCenter)
        self.pokemon_img.setWordWrap(False)
        self.pokemon_img.setObjectName("pokemon_img")
        self.pokemon_img.setPixmap(QtGui.QPixmap('img/init_img.png'))
        self.gridLayout.addWidget(self.pokemon_img, 0, 9, 1, 1)

        # Show text at startup.
        self.text_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_label.sizePolicy().hasHeightForWidth())
        self.text_label.setSizePolicy(sizePolicy)
        self.text_label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.text_label.setAcceptDrops(True)
        self.text_label.setAutoFillBackground(False)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.text_label.setFont(font)
        self.text_label.setText('Choose your team to start a battle!')
        self.text_label.setScaledContents(False)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setWordWrap(False)
        self.text_label.setObjectName("")
        self.gridLayout.addWidget(self.text_label, 0, 7, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 6, 1, 1)

        # Table with Pokemon stats selected in the list.
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 600))
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setStyleSheet("border-style:none")
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        font = QtGui.QFont()
        font.setPointSize(8)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(25)
        item.setFont(font)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        item.setFont(font)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setItem(9, 1, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(55)
        self.tableWidget.verticalHeader().setMinimumSectionSize(40)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 7, 1, 1, QtCore.Qt.AlignVCenter)
        self.tableWidget.hide()

        # Button to start the Battle after choose the team.
        self.widget_battle = QtWidgets.QWidget(self.centralwidget)
        self.widget_battle.setObjectName("widget_battle")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_battle)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_battle = QtWidgets.QPushButton(self.widget_battle)
        self.button_battle.setMinimumSize(QtCore.QSize(0, 50))
        self.button_battle.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.button_battle.setFont(font)
        self.button_battle.setStyleSheet("background-color: #0066ff; border-color: #0066ff; color:#ffffff")
        self.button_battle.setObjectName("button_battle")
        self.horizontalLayout.addWidget(self.button_battle)
        self.gridLayout.addWidget(self.widget_battle, 2, 9, 2, 1)
        self.widget_team = QtWidgets.QWidget(self.centralwidget)

        # Pokeball labels that show the team in real-time.
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_team.sizePolicy().hasHeightForWidth())
        self.widget_team.setSizePolicy(sizePolicy)
        self.widget_team.setMinimumSize(QtCore.QSize(470, 200))
        self.widget_team.setObjectName("widget_team")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_team)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_1 = QtWidgets.QLabel(self.widget_team)
        self.label_1.setMinimumSize(QtCore.QSize(50, 50))
        self.label_1.setMaximumSize(QtCore.QSize(50, 50))
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_1.setScaledContents(True)
        self.label_1.setObjectName("label_1")
        self.gridLayout_2.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_team)
        self.label_4.setMinimumSize(QtCore.QSize(50, 50))
        self.label_4.setMaximumSize(QtCore.QSize(50, 50))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_team)
        self.label_3.setMinimumSize(QtCore.QSize(50, 50))
        self.label_3.setMaximumSize(QtCore.QSize(50, 50))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_team)
        self.label_2.setMinimumSize(QtCore.QSize(50, 50))
        self.label_2.setMaximumSize(QtCore.QSize(50, 50))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_team)
        self.label_6.setMinimumSize(QtCore.QSize(50, 50))
        self.label_6.setMaximumSize(QtCore.QSize(50, 50))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_team)
        self.label_5.setMinimumSize(QtCore.QSize(50, 50))
        self.label_5.setMaximumSize(QtCore.QSize(50, 50))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_team, 1, 7, 3, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        # Add and Remove buttons for select and remove Pokemon in the team.
        self.widget_buttons = QtWidgets.QWidget(self.centralwidget)
        self.widget_buttons.setObjectName("widget_buttons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_buttons)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_pokemon = QtWidgets.QPushButton(self.widget_buttons)
        self.add_pokemon.setMinimumSize(QtCore.QSize(50, 35))
        self.add_pokemon.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.add_pokemon.setFont(font)
        self.add_pokemon.setStyleSheet("background-color: #008500; border-color: #008500; color:#ffffff")
        self.add_pokemon.setAutoDefault(False)
        self.add_pokemon.setObjectName("add_pokemon")
        self.horizontalLayout_2.addWidget(self.add_pokemon)
        self.remove_pokemon = QtWidgets.QPushButton(self.widget_buttons)
        self.remove_pokemon.setMinimumSize(QtCore.QSize(50, 35))
        self.remove_pokemon.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.remove_pokemon.setFont(font)
        self.remove_pokemon.setStyleSheet("background-color: #D60000; border-color: #D60000; color:#ffffff")
        self.remove_pokemon.setObjectName("remove_pokemon")
        self.horizontalLayout_2.addWidget(self.remove_pokemon)
        self.gridLayout.addWidget(self.widget_buttons, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Pokemon Team", "Pokemon Team"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "Moves"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("MainWindow", "HP"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("MainWindow", "Attack"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("MainWindow", "Defense"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("MainWindow", "Sp. Attack"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("MainWindow", "Sp. Defense"))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("MainWindow", "Speed"))
        item = self.tableWidget.item(9, 0)
        item.setText(_translate("MainWindow", "Total"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.add_pokemon.setText(_translate("MainWindow", "Add"))
        self.remove_pokemon.setText(_translate("MainWindow", "Remove"))
        self.button_battle.setText(_translate("MainWindow", "Ready to Battle"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
