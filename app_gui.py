#https://doc.qt.io/qtforpython/PySide2/QtWidgets/QTableWidget.html#
#https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/
#Web Based Implementation of this: https://www.hebcal.com/yahrzeit/

import sys, csv, socket, requests, json, time, calendar
from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets, uic

#This .ui file is created by QTDesigner and then imported here.
#Add new widgets via QTDesigner, save the ui file and then simply reference them here.
qtCreatorFile = "app_gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class hebcal_converter(QtWidgets.QMainWindow, Ui_MainWindow):
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
        #Populate some cells in the table with default text
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem("Before Sunset"))
        self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem("Birthday"))
        self.occasion_list.setCurrentRow(0)
        self.first_name.setFocus()

        ###This section connects events from all the widgets to their
        ###respective functions.
        self.first_name.textChanged.connect(self.first_name_entry)
        self.last_name.textChanged.connect(self.last_name_entry)
        self.occasion_list.itemClicked.connect(self.occasion_select)

        self.hebrew_date_btn.toggled.connect(self.hebrew_date_toggle)
        self.secular_date_btn.toggled.connect(self.secular_date_toggle)
        
        self.secular_calendar.selectionChanged.connect(self.secular_date_select)
        self.before_sunset_radio.toggled.connect(self.before_sunset_toggle)
        self.after_sunset_radio.toggled.connect(self.after_sunset_toggle)        

        self.heb_year_spin_box.valueChanged.connect(self.heb_year_spin_value)
        self.sec_year_spin_box.valueChanged.connect(self.sec_year_spin_value)
        self.convert_date_secular_btn.clicked.connect(self.convert_heb_to_secular)
        
        self.next_row.clicked.connect(self.row_change)
        self.clear_table.clicked.connect(self.delete_table)
        self.clear_row_btn.clicked.connect(self.clear_row)

        self.table_widget.cellClicked.connect(self.row_select)

        self.convert_all_hebrew_btn.clicked.connect(self.convert_all_to_hebrew)
        self.export_csv_btn.clicked.connect(self.export_to_csv)

    def first_name_entry(self):
        '''
        Gets the name entered into the first_name QLineEdit box.
        Enters it into column index 0 in the table widget.
        '''
        first_name = self.first_name.text()
        self.table_widget.setItem(self.row, 0, QtWidgets.QTableWidgetItem(first_name))

    def last_name_entry(self):
        '''
        Gets the last entered into the last_name QLineEdit box.
        Enters it into column index 1 in the table widget.
        '''
        last_name = self.last_name.text()
        self.table_widget.setItem(self.row, 1, QtWidgets.QTableWidgetItem(last_name))

    def occasion_select(self, item):
        '''
        Gets the occasion selected from the occasion_list QListWidget item.
        Enters it into column index 6 in the table widget.
        '''
        occasion = (item.text())
        self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem(occasion))
        
    def secular_date_toggle(self):
        '''
        The secular date is enabled by default.
        When it is selected, features from the hebrew date are disabled.
        '''
        self.secular_calendar.setEnabled(True)
        self.time_of_day_group_box.setEnabled(True)
        self.months_list.setEnabled(False)
        self.day_spin_box.setEnabled(False)
        self.heb_year_spin_box.setEnabled(False)
        self.sec_year_spin_box.setEnabled(False)
        self.convert_date_secular_btn.setEnabled(False)

    def secular_date_select(self):
        '''
        Gets the secular date from the secular_calendar QCalendarWidget and enters the month,
        day and year into the table.
        If the secular date radio toggle is not selected, the calendar is disabled.
        '''
        date = self.secular_calendar.selectedDate()
        month = str(date.month())
        day = str(date.day())
        year = str(date.year())
        self.table_widget.setItem(self.row, 2, QtWidgets.QTableWidgetItem(month)) 
        self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(day))
        self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(year))

    def before_sunset_toggle(self):
        '''
        It's important to know the time of day of the event as the next
        hebrew day starts at sunset.        
        '''
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem("Before Sunset")) 

    def after_sunset_toggle(self):
        '''
        It's important to know the time of day of the event as the next
        hebrew day starts at sunset.        
        '''
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem("After Sunset"))
        
    def hebrew_date_toggle(self):
        '''
        When this is selected, features from the secular date input get disabled.
        The first month is chosen from months_list by default, so that
        convert_date_secular_btn doesn't crash the program if its pushed first.
        '''
        self.secular_calendar.setEnabled(False)
        self.time_of_day_group_box.setEnabled(False)
        self.months_list.setEnabled(True)
        self.day_spin_box.setEnabled(True)
        self.heb_year_spin_box.setEnabled(True)
        self.sec_year_spin_box.setEnabled(True)
        self.convert_date_secular_btn.setEnabled(True)
        self.months_list.setCurrentItem(self.months_list.item(0))

    def heb_year_spin_value(self):
        '''
        Calculates the selected hebrew year's secular equivalent and updates
        the other spin box. Note this is not 100% accurate due to the fact that
        the hebrew year begins sometime in between September/October.
        '''
        year = str(self.heb_year_spin_box.value())
        sec_year = int(year[1:]) + 1240
        self.sec_year_spin_box.setValue(sec_year)
        self.hebrew_sec_label.setText(f"In the year {year}, \nNisan 1 was in {sec_year}.")

    def sec_year_spin_value(self):
        '''
        Calculates the selected secular year's secular equivalent and updates
        the other spin box. Note this is not 100% accurate due to the fact that
        the hebrew year begins sometime in between September/October.
        '''
        year = self.sec_year_spin_box.value()
        heb_year = (year - 1240) + 5000
        self.heb_year_spin_box.setValue(heb_year)
        self.hebrew_sec_label.setText(f"In the year {heb_year}, \nNisan 1 was in {year}.")

    def convert_heb_to_secular(self):
        '''
        If internet connection is detected, convert the hebrew date to its secular equivalent using
        hebcal's API. This fills out the text box.
        '''
        if self.check_internet_connection:
            heb_month = self.months_list.currentItem().text()
            heb_day = str(self.day_spin_box.value())
            heb_year = str(self.heb_year_spin_box.value())

            year, month, day = self.heb_to_greg(heb_year, heb_month, heb_day)
            self.converted_date_text.setPlainText(f"{heb_month} {heb_day}, {heb_year} is the same as\n"
                                                  f"{calendar.month_name[month]} {day}, {year}.")
            self.table_widget.setItem(self.row, 2, QtWidgets.QTableWidgetItem(month)) 
            self.table_widget.setItem(self.row, 3, QtWidgets.QTableWidgetItem(day))
            self.table_widget.setItem(self.row, 4, QtWidgets.QTableWidgetItem(year))
            self.secular_calendar.setSelectedDate(QtCore.QDate(year, month, day))
            self.secular_date_btn.setChecked(True)
        
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("No Internet Connection.")
            msg.setWindowTitle("Error!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()

    def row_change(self):
        '''
        Next Row Button.
        First checks to make sure that the first name, last name and date fields aren't empty.
        Increases the count of rows by 1 and selects the first cell in the newly created row.
        Also enters the currently selected occasion into the occasion field.
        '''
        message = False
        if self.table_widget.item(self.row, 0) == None:
            text = "First Name cannot be empty."
            message = True
        elif ' ' in self.table_widget.item(self.row, 0).text():
            text = "No spaces allowed in First Name."
            message = True
        elif self.table_widget.item(self.row, 1) == None:
            text = "Last Name cannot be empty."
            message = True
        elif ' ' in self.table_widget.item(self.row, 1).text():
            text = "No spaces allowed in Last Name."
            message = True
        elif self.table_widget.item(self.row, 2) == None:
            text = "Date cannot be empty."
            message = True

        if message:
            msg = QtWidgets.QMessageBox()
            msg.setText(text)
            msg.setWindowTitle("Error!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()
            return

        row_amount = self.table_widget.rowCount()
        if self.row + 1 == row_amount:
            self.table_widget.setRowCount(row_amount + 1) 
        self.table_widget.setCurrentCell((self.row + 1),0)
        self.row += 1
        self.current_row_label.setText(f"Current Row: {self.row + 1}")
        #Resets values back to default.
        self.first_name.setText('')
        self.last_name.setText('')
        #Going to the next row fills out the Occassion field with whatever is still currently
        #selected. This makes it convenient to enter rows with the same occassions one after the other.
        #This also prevents a user from having to click away and then click back to choose the
        #currently selected item.
        current_occasion = self.occasion_list.currentItem()
        self.table_widget.setItem(self.row, 6, QtWidgets.QTableWidgetItem(current_occasion.text()))
        self.before_sunset_radio.setChecked(True)
        self.table_widget.setItem(self.row, 5, QtWidgets.QTableWidgetItem("Before Sunset"))

    def row_select(self):
        '''
        When clicking on a cell on the table, it changes the current row to the currently
        selected cell's row.
        Additionally sets the widgets to match what's currently selected in that row.
        '''
        self.row = self.table_widget.currentRow()
        self.current_row_label.setText(f"Current Row: {self.row + 1}")
        #set before/after sunset radio button to match data in table
        if self.table_widget.item(self.row, 5).text() == "Before Sunset":
            self.before_sunset_radio.setChecked(True)
        else:
            self.after_sunset_radio.setChecked(True)
        #set first/last name to match data in table
        #try/except if row is selected before first row is filled out
        try:
            self.first_name.setText(self.table_widget.item(self.row, 0).text())
            self.last_name.setText(self.table_widget.item(self.row, 1).text())
        except AttributeError:
            pass
        #set calendar selection to match date in table
        #try/except if row is selected before first row is filled out
        try:
            month = int(self.table_widget.item(self.row, 2).text())
            day = int(self.table_widget.item(self.row, 3).text())
            year = int(self.table_widget.item(self.row, 4).text())
            self.secular_calendar.setSelectedDate(QtCore.QDate(year, month, day))
        except AttributeError:
            pass
        #Set the currently selected occasion to match what's in the table.
        current_occasion = self.table_widget.item(self.row, 6).text()
        for index in range(self.occasion_list.count()):
            if self.occasion_list.item(index).text() == current_occasion:
                self.occasion_list.setCurrentItem(self.occasion_list.item(index))

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
            for x in range(7):
                self.table_widget.setItem(self.row, x, QtWidgets.QTableWidgetItem(''))
            self.table_widget.setCurrentCell(self.row,0)
            self.first_name.clear()
            self.last_name.clear()
        else:
            self.table_widget.removeRow(self.row)
            self.row -= 1
            self.row_select()

    def convert_all_to_hebrew(self):
        pass

    def export_to_csv(self):
        '''
        Exports data from the table to a csv file.
        Each row number is a dictionary key
        with each full row's list of items as its value.
        '''
        row_list = [x for x in range(self.table_widget.rowCount())]
        table_dict = {i: [] for i in row_list}
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                #A try/except was used here temporarily because the data hasn't been
                #validated yet. Once validation is implemented, there won't be any
                #cells filled with "None."
                try:
                    table_dict[row].append(self.table_widget.item(row, column).text())
                except AttributeError:
                    print('none')
        #QFileDialog creates a pop up window asking the user to select a destination
        #and choose the filename to export the csv. Only a csv is allowed.
        #Each list from the table_dict is written to the csv file.
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File As',"", "csv(*.csv)")
        #If no file is chosen, the program crashes. The try/except prevents that.
        try:
            with open(filename[0], 'w', newline = '') as f:
                csv_writer = csv.writer(f)
                for key in table_dict:
                    csv_writer.writerow(table_dict[key])
        except FileNotFoundError:
            #Exit this function without displaying a success pop up message.
            return
        #Pop up window showing the export was successful.
        msg = QtWidgets.QMessageBox()
        msg.setText("CSV Successfully Exported.")
        msg.setWindowTitle("Success!")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def exception_hook(self, exctype, value, traceback):
        '''
        This function is setup to print silent errors.
        '''
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1)

    def check_internet_connection(self):
        '''
        API calls to hebcal rely on an active internet connection.
        This function checks if a connection can be established or not.
        '''
        try:
            socket.create_connection(("www.hebcal.com", 80))
            return True
        except OSError:
            pass
        return False

    def heb_to_greg(self, year, month, day):
        '''
        Utilizes HebCal's API to convert hebrew dates to gregorian dates
        To convert from Hebrew to Gregorian use this URL format:

        https://www.hebcal.com/converter/?cfg=json&hy=5753&hm=Tamuz&hd=25&h2g=1

        cfg=json – output format is JSON (cfg=json) or XML (cfg=xml)
        hy=5753 – Hebrew year
        hm=Tamuz – Hebrew month (Nisan, Iyyar, Sivan, Tamuz, Av, Elul,
                                 Tishrei, Cheshvan, Kislev, Tevet, Shvat, Adar1, Adar2)
        hd=25 – Hebrew day of month
        h2g=1 – Convert from Hebrew to Gregorian date

        Sample JSON response:
        {'gy': 1993, 'gm': 7, 'gd': 14,
        'hy': 5753, 'hm': 'Tamuz', 'hd': 25,
        'hebrew': 'כ״ה בְּתַמּוּז תשנ״ג', 'events': ['Parashat Matot-Masei']}
        >>>print("Status code:", r.status_code)
        '''
        url = f"https://www.hebcal.com/converter/?cfg=json&hy={year}&hm={month}&hd={day}&h2g=1"
        r = requests.get(url)
        data = r.json()
        secular_year = data['gy']
        secular_month = data['gm']
        secular_day = data['gd']
        return secular_year, secular_month, secular_day

          
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = hebcal_converter()
    window.show()
    sys.exit(app.exec_())
