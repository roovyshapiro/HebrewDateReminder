#https://doc.qt.io/qtforpython/PySide2/QtWidgets/QTableWidget.html#
#https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

#This .ui file is created by QTDesigner and then imported here.
#Add new widgets via QTDesigner, save the ui file and then simply reference them here.
qtCreatorFile = "app_gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #Prints silent errors
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

        ###This section sets certain variables that need to be applied before any
        ###widget is activated.
        #Start the table at 0,0 instead of the default of -1,-1
        self.table_widget.setCurrentCell(0,0)
        #Whichever current row is selected
        self.row = self.table_widget.currentRow()
        self.table_widget.setItem(self.row, 7, QtWidgets.QTableWidgetItem('hebrew'))

        ###This section connects events from all the widgets to their
        ###respective functions.
        self.first_name.textChanged.connect(self.first_name_entry)
        self.last_name.textChanged.connect(self.last_name_entry)
        self.occasion_list.itemClicked.connect(self.occasion_select)
        #Since the two radio buttons are mutually exclusive, we only
        #need to connect it to one function.
        self.hebrew_date_btn.toggled.connect(self.hebrew_date_toggle)
        self.secular_date_btn.toggled.connect(self.secular_date_toggle)
        
        self.months_list.itemClicked.connect(self.months_select)
        self.day_spin_box.valueChanged.connect(self.day_spin_value)

        self.sec_year_radio.toggled.connect(self.sec_year_radio_toggle)
        self.heb_year_radio.toggled.connect(self.heb_year_radio_toggle)

        self.sec_year_spin_box.valueChanged.connect(self.sec_year_spin_value)
        self.heb_year_spin_box.valueChanged.connect(self.heb_year_spin_value)
        
        self.secular_calendar.selectionChanged.connect(self.secular_date_select)
        self.next_row.clicked.connect(self.row_change)
        self.clear_table.clicked.connect(self.delete_table)
        self.clear_row_btn.clicked.connect(self.clear_row)
        self.table_widget.cellClicked.connect(self.row_select)


        
    def first_name_entry(self):
        '''
        Gets the name entered into the first_name QPlainTextEdit box.
        Enters it into column index 0 in the table widget.
        '''
        first_name = self.first_name.toPlainText()
        self.table_widget.setItem(self.row, 0, QtWidgets.QTableWidgetItem(first_name))

    def last_name_entry(self):
        '''
        Gets the last entered into the first_name QPlainTextEdit box.
        Enters it into column index 1 in the table widget.
        '''
        last_name = self.last_name.toPlainText()
        self.table_widget.setItem(self.row, 1, QtWidgets.QTableWidgetItem(last_name))

    def occasion_select(self, item):
        '''
        Gets the occasion selected from the occasion_list QListWidget item.
        Enters it into column index 1 in the table widget.
        '''
        occasion = (item.text())
        self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem(occasion))
        
    def hebrew_date_toggle(self):
        '''
        Enables/Disables relevant features.
        If either the Hebrew Date QRadioButton or the Secular Date QRadioButton is selected,
        the month, day and year fields get cleared out.
        In addition, the Calendar column in the table gets filled out to show which type of
        date entry it is. This will be useful for first converting all secular dates to hebrew
        dates.
        '''
        self.secular_calendar.setEnabled(False)
        self.months_list.setEnabled(True)
        self.day_spin_box.setEnabled(True)
        self.hebyear_groupbox.setEnabled(True)
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem(''))
        
        if self.hebrew_date_btn.isChecked() or self.secular_date_btn.isChecked():
            self.table_widget.setItem(self.row, 2, QtWidgets.QTableWidgetItem(''))
            self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(''))
            self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(''))
        if self.hebrew_date_btn.isChecked():
            self.table_widget.setItem(self.row, 7, QtWidgets.QTableWidgetItem('hebrew'))
        elif self.secular_date_btn.isChecked():
            self.table_widget.setItem(self.row, 7, QtWidgets.QTableWidgetItem('secular'))

    def secular_date_toggle(self):
        '''
        Enables/Disables relevant features.
        '''
        self.secular_calendar.setEnabled(True)
        self.months_list.setEnabled(False)
        self.day_spin_box.setEnabled(False)
        self.hebyear_groupbox.setEnabled(False)
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem('N\A'))
        
    def months_select(self, item):
        '''
        Enters the Hebrew month into the table but only of the Hebrew Date QRadioButton
        is selected. It also sets the day and year files in the table to their default
        values.
        '''
        if self.secular_date_btn.isChecked():
            return
        month = (item.text())
        self.table_widget.setItem(self.row, 2, QtWidgets.QTableWidgetItem(month))
        #Since the spin box for day only goes into effect when the day is changed
        #from the default value of 1, we automatically set the first row day to 1.
        #This will prevent the problem where the first date takes place on the 1st,
        #and it won't be added automatically. We don't have to worry about it for
        #the subsequent rows because row_change auto sets the spin_box back to 1,
        #and that counts as a change.
        self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(1)))
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str(5779)))

    def day_spin_value(self):
        '''
        Gets the day from the day_spin_box QSpinBox and enters it into the table.
        Only works if the Hebrew Date QRadioButton is selected.
        '''
        if self.secular_date_btn.isChecked():
            return
        day = str(self.day_spin_box.value())
        self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(day))

    def sec_year_radio_toggle(self):
        '''
        Allows inputting of Secular year.
        Dissallows inputting of Hebrew Year.
        Every time this button is toggled, the Year value gets reset.
        '''
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(''))
        self.heb_year_spin_box.setEnabled(False)
        self.sec_year_spin_box.setEnabled(True)
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem('secular'))


    def heb_year_radio_toggle(self):
        '''
        Allows inputting of Hebrew Year.
        Dissallows inputting of Secular Year.
        '''
        self.sec_year_spin_box.setEnabled(False)
        self.heb_year_spin_box.setEnabled(True)
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem('hebrew'))

    def heb_year_spin_value(self):
        '''
        Gets the year from the heb_year_spin_box QSpinBox and enters it into the table.
        Only works if the Hebrew Date QRadioButton is selected.
        '''
        if self.secular_date_btn.isChecked() or self.sec_year_radio.isChecked():
            return
        year = str(self.heb_year_spin_box.value())
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(year))

    def sec_year_spin_value(self):
        if self.secular_date_btn.isChecked() or self.heb_year_radio.isChecked():
            return
        year = str(self.sec_year_spin_box.value())
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(year))

    def secular_date_select(self):
        '''
        Gets the secular date from the secular_calendar QCalendarWidget and enters the month,
        day and year into the table.
        Only works if the Secular Date QRadioButton is selected.
        '''
        if self.hebrew_date_btn.isChecked():
            return
        date = self.secular_calendar.selectedDate()
        month = str(date.month())
        day = str(date.day())
        year = str(date.year())
        self.table_widget.setItem(self.row, 2, QtWidgets.QTableWidgetItem(month)) 
        self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(day))
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(year))
        

    def row_change(self):
        '''
        Next Row Button.
        Increases the count of rows by 1 and selects the first cell in the newly created row.
        Also resets the hebrew spin box values back to default.
        Also enters the currently selected occasion into the occasion field.
        '''
        row_amount = self.table_widget.rowCount()
        if self.row + 1 == row_amount:
            self.table_widget.setRowCount(row_amount + 1) 
        self.table_widget.setCurrentCell((self.row + 1),0)
        self.row += 1
        self.current_row_label.setText(f"Current Row: {self.row + 1}")
        #Resets values back to default.
        #These fill in the next row if possible since it counts as a value change.
        self.day_spin_box.setValue(1)
        self.heb_year_spin_box.setValue(5779)
        self.first_name.setPlainText('')
        self.last_name.setPlainText('')
        #Going to the next row fills out the Occassion field with whatever is still currently
        #selected. This makes it convenient to enter rows with the same occassions one after the other.
        #This also prevents a user from having to click away and then click back to choose the
        #currently selected item.
        current_occasion = self.occasion_list.currentItem()
        #If "Next Row" is selected prior to the occasion is selected,
        #the Occasion value will be set to blank. Otherwise it's None by default
        #and none has no .text() function and the program crashes silently.
        try:
            self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem(current_occasion.text()))
        except AttributeError:
            self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem(''))

        if self.hebrew_date_btn.isChecked():
            self.table_widget.setItem(self.row, 7, QtWidgets.QTableWidgetItem('hebrew'))
        elif self.secular_date_btn.isChecked():
            self.table_widget.setItem(self.row, 7, QtWidgets.QTableWidgetItem('secular'))

    def row_select(self):
        '''
        When clicking on a cell on the table, it changes the current row to the currently
        selected cell's row.
        '''
        self.row = self.table_widget.currentRow()
        self.current_row_label.setText(f"Current Row: {self.row + 1}")

    def delete_table(self):
        '''
        Clears the contents of the entire table.
        '''
        self.table_widget.clearContents()
        self.table_widget.setCurrentCell(0,0)

    def clear_row(self):
        '''
        Deletes the selected row.
        If only one row is left, it is cleared instead.
        '''
        if self.table_widget.rowCount() <= 1:
            for x in range(8):
                self.table_widget.setItem(self.row, x, QtWidgets.QTableWidgetItem(''))
            self.table_widget.setCurrentCell(self.row,0)
            self.first_name.clear()
            self.last_name.clear()
        else:
            self.table_widget.removeRow(self.row)

    def exception_hook(self, exctype, value, traceback):
        '''
        This function is setup to print silent errors.
        '''
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1) 
    
          
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
