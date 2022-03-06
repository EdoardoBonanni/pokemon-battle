# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_item_list.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_item(object):
    def setupUi(self, widget_item):
        widget_item.setObjectName("widget_item")
        widget_item.resize(280, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget_item.sizePolicy().hasHeightForWidth())
        widget_item.setSizePolicy(sizePolicy)
        widget_item.setMinimumSize(QtCore.QSize(240, 10))
        widget_item.setMaximumSize(QtCore.QSize(240, 60))
        # widget_item.setMaximumSize(QtCore.QSize(300, 300))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(widget_item)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_gif = QtWidgets.QLabel(widget_item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_gif.sizePolicy().hasHeightForWidth())
        self.label_gif.setSizePolicy(sizePolicy)
        # self.label_gif.setMinimumHeight(10)
        self.label_gif.setMaximumSize(QtCore.QSize(50, 50))
        self.label_gif.setMinimumSize(QtCore.QSize(50, 50))
        self.label_gif.setScaledContents(True)
        self.label_gif.setObjectName("label_gif")
        self.horizontalLayout_2.addWidget(self.label_gif)
        self.label_name = QtWidgets.QLabel(widget_item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setScaledContents(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout_2.addWidget(self.label_name)

        self.retranslateUi(widget_item)
        QtCore.QMetaObject.connectSlotsByName(widget_item)

    def retranslateUi(self, widget_item):
        _translate = QtCore.QCoreApplication.translate
        widget_item.setWindowTitle(_translate("widget_item", "Form"))
        self.label_gif.setText(_translate("widget_item", "TextLabel"))
        self.label_name.setText(_translate("widget_item", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_item = QtWidgets.QWidget()
    ui = Ui_widget_item()
    ui.setupUi(widget_item)
    widget_item.show()
    sys.exit(app.exec_())

