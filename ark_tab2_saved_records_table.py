# Functions for Tab1 Form
# These functions sets up the database and adds the inputs to the DB
# This module will then be imported from the main.py file
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,QHeaderView, QFileDialog,
                             QAbstractScrollArea, QTableWidget,QMessageBox, QColumnView,
                             QTableWidgetItem, QLabel, QLineEdit, QHBoxLayout,QScrollArea)
import sys
import sqlite3
from ark_update_record_table_window_class import UpdateWindow
from ark_custom_message_box_class import customMessage
import pandas as pd
import openpyxl


class Tab2(QWidget):
    def __init__(self):
        super().__init__()

        # Display Records from the Database
        self.table = QTableWidget()

        # set no of columns
        self.table.setColumnCount(91)

        # this function sets the column width
        self.columnWidthFunction()

        # set column names

        self.table.setHorizontalHeaderLabels(['File No.', 'Company Name', 'Company Old Name', 'Registered No', 'Date of Name Change', 'Date of Incorporation',
        'Company Status', 'Registration Address', 'Business Address', 'Nature of Bussiness', 'Paid Up Capital', 'Member 1', 'No of Shares', 'Member 2', 'No of Shares',
        'Member 3', 'No of Shares', 'Member 4', 'No of Shares', 'Member 5', 'No of Shares', 'Director 1', 'Director 2', 'Director 4', 'Director 4', 'Director 5',
        'Secretaries 1', 'Secretaries 1 Appointed Date','Secretaries 1 Resigned Date','Secretaries 1 Vacated Date', 'Secretaries 2',
        'Secretaries 2 Appointed Date', 'Secretaries 2 Resigned Date','Secretaries 2 Vacated Date',
        'Contact Name', 'Contact Phone','Contact Email', 'Prepared By', 'Prepared Date',
        'Scanned By', 'Scanned Date', 'Checked By', 'Checked Date', 'Directors Circular','Members Meeting', 'Register', 'Share Certificate',
        'Summary', 'Checklist', 'Correspondence', 'Bill_SOA', 'SSM_Receipt', 'Application Of Reg',
        'Availability Names Reg', 'Application Change Name', 'Lodgement Constitution', 'Notify Alteration Amendment', 'Change Reg Add',
        'Not at Reg Add', 'Change Add Reg Are Kept', 'Change Reg of Members', 'Change Reg Dir Mgr Sec', 'Annual Return of Company',
        'Approval for Allotment', 'Return for Allotment', 'Variation Class of Rights', 'Instrument of Transfer', 'Solvency Statement',
        'Declaration Appnt as Director', 'Notice Contract Serv Director', 'Declaration Appnt as Secretary', 'Vacate Office of Secretary',
        'Dec by Sec to Cease Off', 'Reg to Act as Sec', 'Diff Accounting Periods', 'EOT Financial Statements', 'Exempt Private Company',
        'Lodge with Charge', 'Series of Debentures', 'Assignment of Charge', 'Variations Terms of Change', 'Property Undertaking Memo',
        'Memo Satisfaction Reg Charge', 'Dec Verifying Memo', 'Satisfaction of Charge', 'Strike of Company', 'Object Striking of Company',
        'Withdraw Striking of Company', 'Change in Bus Add or Nature of Bus', 'File 47', 'Temporary Folder'])

        self.refreshRecordsBtn = QPushButton('Refresh Records')
        self.refreshRecordsBtn.clicked.connect(self.loadData)

        self.deepViewUpdateBtn = QPushButton('Update Record')
        self.deepViewUpdateBtn.clicked.connect(self.deepViewWithBriefLayout)

        self.exportToCSVBtn = QPushButton("Export to Spreadsheet")
        self.exportToCSVBtn.clicked.connect(self.exportToCSVFunction)

        self.deleteSelectedRecord = QPushButton("Delete Selected Record")
        self.deleteSelectedRecord.clicked.connect(self.deleteRecordWarningMessage)

        self.openFolderSelectedRecord = QPushButton("View Folders")
        self.openFolderSelectedRecord.clicked.connect(self.openFileFolderButton)


        self.mainLayoutTab2 = QVBoxLayout()
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.table)
        # self.tableLayout.addSpacing(50)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.addWidget(self.refreshRecordsBtn)
        self.buttonHLayout.addWidget(self.deepViewUpdateBtn)
        self.buttonHLayout.addWidget(self.exportToCSVBtn)
        self.buttonHLayout.addWidget(self.deleteSelectedRecord)
        self.buttonHLayout.addWidget(self.openFolderSelectedRecord)
        self.mainLayoutTab2.addLayout(self.tableLayout)
        self.mainLayoutTab2.addSpacing(30)
        self.mainLayoutTab2.addLayout(self.buttonHLayout)

        self.setLayout(self.mainLayoutTab2)
        self.loadData()


    def columnWidthFunction(self):
    # this sets the individual column widths, you cannot uset f string or else it cannot read an integer

        for col in range(0, 92):
            column_width = 250
            self.table.setColumnWidth(col, column_width)

    def deepViewWithBriefLayout(self):

        try:
            self.getRowForDeepView()

            selectedRowToDeepView = [self.field1, self.field2, self.field3, self.field4,
                  self.field5, self.field6, self.field7, self.field8, self.field9,
                  self.field10, self.field11, self.field12, self.field13, self.field14,
                  self.field15, self.field16, self.field17, self.field18, self.field19,
                  self.field20, self.field21, self.field22, self.field23, self.field24,
                  self.field25, self.field26, self.field27, self.field28, self.field29,
                  self.field30, self.field31, self.field32, self.field33, self.field34,
                  self.field35, self.field36, self.field37, self.field38, self.field39,
                  self.field40, self.field41, self.field42, self.field43]

            selectedRow =  self.selectedRow
            self.window2 = UpdateWindow(selectedRowToDeepView)
            self.window2.show()
        except:
            pass

    def openFileFolderButton(self):
        # this function opens the selected company's file folder using QFileDialog

        try:
            self.selectedRow = self.table.currentRow() # gets the selected row (highlighted)
            self.field2 = self.table.item(self.selectedRow, 1).text() # extracts the company name
            folder_name = f'{self.field2}_DocFolder' # uses string formatting to get the selected companies name

            # Open File Dialog
            # Uses QFileDialog to open the respective company's file folder
            # QFileDialog.getExistingDirectory(self, 'Selected Folder Opened', f'.//ScannedDocs//{folder_name}')
            QFileDialog.getOpenFileNames(self, 'Selected Folder Opened', f'.//ScannedDocs//{folder_name}', 'All Files (*)')

        except:
            customMessage('You have not selected a row with a Company from the table above, please select a row and try again')

    def deleteRecordFunction(self):
        # this deletes the selected record

        try:
            self.selectedRow = self.table.currentRow()


            self.field1 = self.table.item(self.selectedRow, 0).text()
            self.field2 = self.table.item(self.selectedRow, 1).text()

            self.databaseName = 'ark_db'
            self.databaseName = f'{self.databaseName}.db'
            self.tableName = 'ark_table'

            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()
            self.c.execute(f"""DELETE FROM {self.tableName} WHERE FileNo = '{self.field1}' """)

            self.conn.commit()
            self.table.removeRow(self.selectedRow)

            customMessage(f"Deleted all records belonging to Company {self.field2}")

        except:
            print('Please select the record you would like to delete')

    def deleteRecordWarningMessage(self):
        # this is the warning message before deleting selected record, if selected Yes, this will execute the delete function
        deleteWarningMessage = QMessageBox.question(self, 'Warning!', 'Are you sure you want to delete this record?' 
                                                                      ' This action cannot be undone',
                                                    QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

        if deleteWarningMessage == QMessageBox.Yes:
            self.deleteRecordFunction()

    def loadData(self):

        ######################################################
        # new db
        ######################################################

        self.con = sqlite3.connect("ark_db.db")
        self.cur = self.con.cursor()
        self.query = "SELECT * FROM ark_table"
        self.cur.execute(self.query)

        self.table.setRowCount(100)
        tableRowIndex = 0
        for row in self.cur.execute(self.query):
            self.table.setItem(tableRowIndex, 0, QTableWidgetItem(row[0]))
            self.table.setItem(tableRowIndex, 1, QTableWidgetItem(row[1]))
            self.table.setItem(tableRowIndex, 2, QTableWidgetItem(row[2]))
            self.table.setItem(tableRowIndex, 3, QTableWidgetItem(row[3]))
            self.table.setItem(tableRowIndex, 4, QTableWidgetItem(row[4]))
            self.table.setItem(tableRowIndex, 5, QTableWidgetItem(row[5]))
            self.table.setItem(tableRowIndex, 6, QTableWidgetItem(row[6]))
            self.table.setItem(tableRowIndex, 7, QTableWidgetItem(row[7]))
            self.table.setItem(tableRowIndex, 8, QTableWidgetItem(row[8]))
            self.table.setItem(tableRowIndex, 9, QTableWidgetItem(row[9]))
            self.table.setItem(tableRowIndex, 10, QTableWidgetItem(row[10]))
            self.table.setItem(tableRowIndex, 11, QTableWidgetItem(row[11]))
            self.table.setItem(tableRowIndex, 12, QTableWidgetItem(row[12]))
            self.table.setItem(tableRowIndex, 13, QTableWidgetItem(row[13]))
            self.table.setItem(tableRowIndex, 14, QTableWidgetItem(row[14]))
            self.table.setItem(tableRowIndex, 15, QTableWidgetItem(row[15]))
            self.table.setItem(tableRowIndex, 16, QTableWidgetItem(row[16]))
            self.table.setItem(tableRowIndex, 17, QTableWidgetItem(row[17]))
            self.table.setItem(tableRowIndex, 18, QTableWidgetItem(row[18]))
            self.table.setItem(tableRowIndex, 19, QTableWidgetItem(row[19]))
            self.table.setItem(tableRowIndex, 20, QTableWidgetItem(row[20]))
            self.table.setItem(tableRowIndex, 21, QTableWidgetItem(row[21]))
            self.table.setItem(tableRowIndex, 22, QTableWidgetItem(row[22]))
            self.table.setItem(tableRowIndex, 23, QTableWidgetItem(row[23]))
            self.table.setItem(tableRowIndex, 24, QTableWidgetItem(row[24]))
            self.table.setItem(tableRowIndex, 25, QTableWidgetItem(row[25]))
            self.table.setItem(tableRowIndex, 26, QTableWidgetItem(row[26]))
            self.table.setItem(tableRowIndex, 27, QTableWidgetItem(row[27]))
            self.table.setItem(tableRowIndex, 28, QTableWidgetItem(row[28]))
            self.table.setItem(tableRowIndex, 29, QTableWidgetItem(row[29]))
            self.table.setItem(tableRowIndex, 30, QTableWidgetItem(row[30]))
            self.table.setItem(tableRowIndex, 31, QTableWidgetItem(row[31]))
            self.table.setItem(tableRowIndex, 32, QTableWidgetItem(row[32]))
            self.table.setItem(tableRowIndex, 33, QTableWidgetItem(row[33]))
            self.table.setItem(tableRowIndex, 34, QTableWidgetItem(row[34]))
            self.table.setItem(tableRowIndex, 35, QTableWidgetItem(row[35]))
            self.table.setItem(tableRowIndex, 36, QTableWidgetItem(row[36]))
            self.table.setItem(tableRowIndex, 37, QTableWidgetItem(row[37]))
            self.table.setItem(tableRowIndex, 38, QTableWidgetItem(row[38]))
            self.table.setItem(tableRowIndex, 39, QTableWidgetItem(row[39]))
            self.table.setItem(tableRowIndex, 40, QTableWidgetItem(row[40]))
            self.table.setItem(tableRowIndex, 41, QTableWidgetItem(row[41]))
            self.table.setItem(tableRowIndex, 42, QTableWidgetItem(row[42]))
            self.table.setItem(tableRowIndex, 43, QTableWidgetItem(row[43]))
            self.table.setItem(tableRowIndex, 44, QTableWidgetItem(row[44]))
            self.table.setItem(tableRowIndex, 45, QTableWidgetItem(row[45]))
            self.table.setItem(tableRowIndex, 46, QTableWidgetItem(row[46]))
            self.table.setItem(tableRowIndex, 47, QTableWidgetItem(row[47]))
            self.table.setItem(tableRowIndex, 48, QTableWidgetItem(row[48]))
            self.table.setItem(tableRowIndex, 49, QTableWidgetItem(row[49]))
            self.table.setItem(tableRowIndex, 50, QTableWidgetItem(row[50]))
            self.table.setItem(tableRowIndex, 51, QTableWidgetItem(row[51]))
            self.table.setItem(tableRowIndex, 52, QTableWidgetItem(row[52]))
            self.table.setItem(tableRowIndex, 53, QTableWidgetItem(row[53]))
            self.table.setItem(tableRowIndex, 54, QTableWidgetItem(row[54]))
            self.table.setItem(tableRowIndex, 55, QTableWidgetItem(row[55]))
            self.table.setItem(tableRowIndex, 56, QTableWidgetItem(row[56]))
            self.table.setItem(tableRowIndex, 57, QTableWidgetItem(row[57]))
            self.table.setItem(tableRowIndex, 58, QTableWidgetItem(row[58]))
            self.table.setItem(tableRowIndex, 59, QTableWidgetItem(row[59]))
            self.table.setItem(tableRowIndex, 60, QTableWidgetItem(row[60]))
            self.table.setItem(tableRowIndex, 61, QTableWidgetItem(row[61]))
            self.table.setItem(tableRowIndex, 62, QTableWidgetItem(row[62]))
            self.table.setItem(tableRowIndex, 63, QTableWidgetItem(row[63]))
            self.table.setItem(tableRowIndex, 64, QTableWidgetItem(row[64]))
            self.table.setItem(tableRowIndex, 65, QTableWidgetItem(row[65]))
            self.table.setItem(tableRowIndex, 66, QTableWidgetItem(row[66]))
            self.table.setItem(tableRowIndex, 67, QTableWidgetItem(row[67]))
            self.table.setItem(tableRowIndex, 68, QTableWidgetItem(row[68]))
            self.table.setItem(tableRowIndex, 69, QTableWidgetItem(row[69]))
            self.table.setItem(tableRowIndex, 70, QTableWidgetItem(row[70]))
            self.table.setItem(tableRowIndex, 71, QTableWidgetItem(row[71]))
            self.table.setItem(tableRowIndex, 72, QTableWidgetItem(row[72]))
            self.table.setItem(tableRowIndex, 73, QTableWidgetItem(row[73]))
            self.table.setItem(tableRowIndex, 74, QTableWidgetItem(row[74]))
            self.table.setItem(tableRowIndex, 75, QTableWidgetItem(row[75]))
            self.table.setItem(tableRowIndex, 76, QTableWidgetItem(row[76]))
            self.table.setItem(tableRowIndex, 77, QTableWidgetItem(row[77]))
            self.table.setItem(tableRowIndex, 78, QTableWidgetItem(row[78]))
            self.table.setItem(tableRowIndex, 79, QTableWidgetItem(row[79]))
            self.table.setItem(tableRowIndex, 80, QTableWidgetItem(row[80]))
            self.table.setItem(tableRowIndex, 81, QTableWidgetItem(row[81]))
            self.table.setItem(tableRowIndex, 82, QTableWidgetItem(row[82]))
            self.table.setItem(tableRowIndex, 83, QTableWidgetItem(row[83]))
            self.table.setItem(tableRowIndex, 84, QTableWidgetItem(row[84]))
            self.table.setItem(tableRowIndex, 85, QTableWidgetItem(row[85]))
            self.table.setItem(tableRowIndex, 86, QTableWidgetItem(row[86]))
            self.table.setItem(tableRowIndex, 87, QTableWidgetItem(row[87]))
            self.table.setItem(tableRowIndex, 88, QTableWidgetItem(row[88]))
            self.table.setItem(tableRowIndex, 89, QTableWidgetItem(row[89]))
            self.table.setItem(tableRowIndex, 90, QTableWidgetItem(row[90]))


            tableRowIndex += 1

    def getRowForDeepView(self):

        try:
            self.selectedRow = self.table.currentRow()

            self.field1 = self.table.item(self.selectedRow, 0).text()
            self.field2 = self.table.item(self.selectedRow, 1).text()
            self.field3 = self.table.item(self.selectedRow, 2).text()
            self.field4 = self.table.item(self.selectedRow, 3).text()
            self.field5 = self.table.item(self.selectedRow, 4).text()
            self.field6 = self.table.item(self.selectedRow, 5).text()
            self.field7 = self.table.item(self.selectedRow, 6).text()
            self.field8 = self.table.item(self.selectedRow, 7).text()
            self.field9 = self.table.item(self.selectedRow, 8).text()
            self.field10 = self.table.item(self.selectedRow, 9).text()
            self.field11 = self.table.item(self.selectedRow, 10).text()
            self.field12 = self.table.item(self.selectedRow, 11).text()
            self.field13 = self.table.item(self.selectedRow, 12).text()
            self.field14 = self.table.item(self.selectedRow, 13).text()
            self.field15 = self.table.item(self.selectedRow, 14).text()
            self.field16 = self.table.item(self.selectedRow, 15).text()
            self.field17 = self.table.item(self.selectedRow, 16).text()
            self.field18 = self.table.item(self.selectedRow, 17).text()
            self.field19 = self.table.item(self.selectedRow, 18).text()
            self.field20 = self.table.item(self.selectedRow, 19).text()
            self.field21 = self.table.item(self.selectedRow, 20).text()
            self.field22 = self.table.item(self.selectedRow, 21).text()
            self.field23 = self.table.item(self.selectedRow, 22).text()
            self.field24 = self.table.item(self.selectedRow, 23).text()
            self.field25 = self.table.item(self.selectedRow, 24).text()
            self.field26 = self.table.item(self.selectedRow, 25).text()
            self.field27 = self.table.item(self.selectedRow, 26).text()
            self.field28 = self.table.item(self.selectedRow, 27).text()
            self.field29 = self.table.item(self.selectedRow, 28).text()
            self.field30 = self.table.item(self.selectedRow, 29).text()
            self.field31 = self.table.item(self.selectedRow, 30).text()
            self.field32 = self.table.item(self.selectedRow, 31).text()
            self.field33 = self.table.item(self.selectedRow, 32).text()
            self.field34 = self.table.item(self.selectedRow, 33).text()
            self.field35 = self.table.item(self.selectedRow, 34).text()
            self.field36 = self.table.item(self.selectedRow, 35).text()
            self.field37 = self.table.item(self.selectedRow, 36).text()
            self.field38 = self.table.item(self.selectedRow, 37).text()
            self.field39 = self.table.item(self.selectedRow, 38).text()
            self.field40 = self.table.item(self.selectedRow, 39).text()
            self.field41 = self.table.item(self.selectedRow, 40).text()
            self.field42 = self.table.item(self.selectedRow, 41).text()
            self.field43 = self.table.item(self.selectedRow, 42).text()
            self.field43 = self.table.item(self.selectedRow, 43).text()
            self.field43 = self.table.item(self.selectedRow, 44).text()
            self.field43 = self.table.item(self.selectedRow, 45).text()


        except:
            customMessage('Please select a record to be displayed')

    def exportToCSVFunction(self):

        ######################################################
        # new db
        ######################################################

        self.tableName = 'ark_table'
        sqlite_db = sqlite3.connect('ark_db.db')
        df = pd.read_sql_query(f""" SELECT * FROM {self.tableName}""", sqlite_db)

        df.to_excel(f'{self.tableName}.xlsx')




