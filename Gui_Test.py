import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(600,200,500,300)
        self.setWindowTitle("HebrewDateConverter")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        extractAction = QtGui.QAction('&Exit!', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave The Application')
        extractAction.triggered.connect(self.close_application)
        
        extractAction2 = QtGui.QAction('&test!', self)
        extractAction2.triggered.connect(self.test_func)
        extractAction2.setShortcut('Ctrl+C')
                
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        object_menu = mainMenu.addMenu('&Test')
        fileMenu.addAction(extractAction)
        object_menu.addAction(extractAction2)

                
        self.home()

    def home(self):
        btn = QtGui.QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        #btn.resize(50,50)
        #btn.resize(btn.sizeHint())
        btn.resize(btn.minimumSizeHint())
        btn.move(0,53)

        
        extractAction = QtGui.QAction(QtGui.QIcon('icon.png'), 'Prints Cool', self)
        extractAction.triggered.connect(self.test_func)

        self.toolbar = self.addToolBar('Ext')
        self.toolbar.addAction(extractAction)

        
        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Title','Quit?',QtGui.QMessageBox.Yes , QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            self.test_func()
        
    def test_func(self):
        print('cool')



def run():
    app = QtGui.QApplication([])
    GUI = Window()
    sys.exit(app.exec_())

run()
