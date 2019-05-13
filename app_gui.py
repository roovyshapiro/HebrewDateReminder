#https://doc.qt.io/qtforpython/PySide2/QtWidgets/QTableWidget.html#
#https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

import sys
from PyQt4 import QtCore, QtGui, uic
 
qtCreatorFile = "app_gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.first_name.textChanged.connect(self.first_name_entry)
        self.last_name.textChanged.connect(self.last_name_entry)
        self.months_list.itemClicked.connect(self.months_select)
        self.day_spin_box.valueChanged.connect(self.day_spin_value)
        self.year_spin_box.valueChanged.connect(self.year_spin_value)
        self.occasion_list.itemClicked.connect(self.occasion_select)
        #Start the table at 0,0 instead of the default of -1,-1
        self.table_widget.setCurrentCell(0,0)
        #Whichever current row is selected
        self.row = self.table_widget.currentRow()
        self.next_row.clicked.connect(self.row_change)
        self.clear_table.clicked.connect(self.delete_table)
        
    def first_name_entry(self):
        first_name = self.first_name.toPlainText()
        self.table_widget.setItem(self.row, 0, QtGui.QTableWidgetItem(first_name))

    def last_name_entry(self):
        last_name = self.last_name.toPlainText()
        self.table_widget.setItem(self.row, 1, QtGui.QTableWidgetItem(last_name))

    def months_select(self, item):
        month = (item.text())
        self.table_widget.setItem(self.row, 2, QtGui.QTableWidgetItem(month))
        #Since the spin box for day only goes into effect when the day is changed
        #from the default value of 1, we automatically set the first row day to 1.
        #This will prevent the problem where the first date takes place on the 1st,
        #and it won't be added automatically. We don't have to worry about it for
        #the subsequent rows because row_change auto sets the spin_box back to 1,
        #and that counts as a change.
        self.table_widget.setItem(self.row, 3, QtGui.QTableWidgetItem(str(1)))
        self.table_widget.setItem(self.row, 4, QtGui.QTableWidgetItem(str(5779)))

    def day_spin_value(self):
        day = str(self.day_spin_box.value())
        self.table_widget.setItem(self.row, 3, QtGui.QTableWidgetItem(day))

    def year_spin_value(self):
        year = str(self.year_spin_box.value())
        self.table_widget.setItem(self.row, 4, QtGui.QTableWidgetItem(year))

    def occasion_select(self, item):
        occasion = (item.text())
        self.table_widget.setItem(self.row, 5, QtGui.QTableWidgetItem(occasion))

    def row_change(self):
        row_amount = self.table_widget.rowCount()
        if self.row + 1 == row_amount:
            self.table_widget.setRowCount(row_amount + 1) 
        self.table_widget.setCurrentCell((self.row + 1),0)
        self.row += 1
        #Resets values back to default.
        #These fill in the next row if possible since it counts as a value change.
        self.day_spin_box.setValue(1)
        self.year_spin_box.setValue(5779)
        self.first_name.setPlainText('')
        self.last_name.setPlainText('')
              
    def delete_table(self):
        self.table_widget.clearContents()
        self.table_widget.setCurrentCell(0,0)

          
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
