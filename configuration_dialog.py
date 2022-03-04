from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
from UI.DialogConfigurationUI import Ui_Dialog
import socket
from urllib.request import urlopen


class configuration_dialog(QDialog):
    def __init__(self, parent=None):
        super(configuration_dialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.set_ip()
        self.interaction()

    def interaction(self):
        self.ui.buttonBox.buttons()[0].clicked.connect(self.dosomething)
        self.ui.buttonBox.buttons()[1].clicked.connect(self.close_dialog)

    def dosomething(self):
        print('ok')

    def close_dialog(self):
        self.close()

    def set_ip(self):
        localhost_game_choose = True
        if localhost_game_choose:
            self.localhost_game()
        else:
            self.online_game()

    def localhost_game(self):
        # Local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print("local_ip: " + str(local_ip))
        self.ui.label_ip.setText("Your IP address: " + str(local_ip))

    def online_game(self):
        # Public IP
        pub_ip = urlopen('http://ip.42.pl/raw').read()
        pub_ip = str(pub_ip).replace('b\'', '').replace('\'', '')
        print("pub_ip: " + pub_ip)
        self.ui.label_ip.setText("Your IP address: " + str(pub_ip))



