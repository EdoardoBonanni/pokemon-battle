import sys
import requests
# from PyQt4 import QtGui, QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QComboBox, QPushButton, QLabel, QDesktopWidget
from myPokedex import myPokedex
from PyQt5.QtGui import QMovie

class PokeDex(QWidget):

    def __init__(self):
        super(PokeDex, self).__init__()

        self.initUI()

    def initUI(self):
        '''Initial UI'''

        # Grid Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.pokedex = myPokedex()
        self.pokedex.readCSV("Kanto Pokemon Spreadsheet.csv")

        # Drop Down
        self.dropdown = QComboBox(self)
        self.names = list(self.pokedex.listaPokemon.keys())
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0,0,1,1)

        # Search Button
        self.btn = QPushButton('Search', self)
        self.btn.clicked.connect(self.runSearch)
        self.grid.addWidget(self.btn, 0,1,1,1)

        # Image
        self.img = QLabel(self)
        self.grid.addWidget(self.img, 1,1,1,1)

        # Data
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('\nName:\n\nType1:\n\nType2:\n\nHP:\n\nAttack\n\nSp. Attack\n\n Defense:\n\nSp. Defense:\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1,0,1,1)

        # Customize Widgets
        self.resize(500, 250)
        self.center()
        self.setWindowTitle('PokeDex')
        self.show()

    def runSearch(self):
        '''Event for run button'''

        #Parse value
        index = self.dropdown.currentIndex()
        item_name = self.names[index]

        item = self.pokedex.listaPokemon[item_name]

        # Movie
        # dir_sprites = 'Sprites/'
        # img_name = dir_sprites + item_name.lower() + '.gif'
        # self.img.setPixmap(QtGui.QPixmap(img_name))
        self.movie = QMovie('Sprites/' + item_name.lower() + '.gif')
        self.img.setMovie(self.movie)
        self.movie.start()

        # Set values
        name = 'Name:\t\t\t'+item_name+'\n\n'
        type1 = 'Type1:\t\t\t'+ str(item.type1) +'\n\n'
        type2 = 'Type2:\t\t\t'+ str(item.type2) +'\n\n'
        hp = 'HP:\t\t\t'+ str(item.hp) + '\n\n'
        atk = 'Attack:\t\t\t'+ str(item.atk) + '\n\n'
        satk = 'Sp. Attack:\t\t'+ str(item.spAtk) + '\n\n'
        deff = 'Defense:\t\t\t'+ str(item.defense) + '\n\n'
        sdef = 'Sp. Defense:\t\t'+ str(item.spDef) + '\n\n'
        speed = 'Speed:\t\t\t'+ str(item.speed) + '\n\n'
        total = 'Total:\t\t\t'+ str(item.total) + '\n\n'

        # Add text
        final = name+type1+type2+hp+atk+satk+deff+sdef+speed+total
        self.label.setText(final)

    def center(self):
        '''Center Widget on screen'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    '''Codes for running GUI'''

    # Create Application object to run GUI
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.aboutToQuit.connect(app.deleteLater)

    # Run GUI
    gui = PokeDex()
    # Exit cleanly when closing GUI
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()