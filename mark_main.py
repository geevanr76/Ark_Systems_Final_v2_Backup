"""
    version date: 14th Aug 2022
    version updates: refactoring of code with new file names and 48 folders + temporary/misc instead of
    previous 47 + temporary/miscellaneous
    note: this was originally done in kali linux, hence changes from '//' in windows to '\' was made to os.path in
    following files [ark_main.py, ark_stacked_filing_system_backend_class.py, ark_tab_1_company_brief.py ]

    1) files that list all folder names = [ark_stacked_filing_system_frontend, ark_tab1_company_brief.py,
                    ark_tab2_saved_records.py, ark_db_table_and_input_class.py]

    2) Remove Delete and delete all [ark_main_ui_class-line: 372-373 & 407]

    databaseName = 'ark_db.db'
    databaseTable = 'ark_table'

    Improvements to be added on to the new version
    a) Limit to only one instance
    b) Saved records = 12 columns - done
    c) Add 2 more options as checkboxes or pull down menu to the stacked filing system for Dir and Mem - done
    d) Increase to 5 Directors
    e) Check if we can improve on the file no and co name validation - done
    f) Check on the status radio button failures - done
    g) Would it be possible to change the date to a calendar date picker format

    Ark_2.0_v1
    c) Currently the date selectors for tab 1, filling widget, and update window, may be allowing for dates earlier than necessary for example 1900,and dates
     later than the current date which would not serve and need for our application. Hence, it would be great if it is possible to set an earliest date and latest
     date possible
    d) Limit to only one instance
    f) Would it be possible to change the date to a calendar date picker format. also check the current format, it should be dd/mm/yyyy
    g) For the update record window, after clicking on update, the record updates in the db but it doesnt immediately refresh the updated record,
       it would be great if we could automatically refresh the window with the updated record, as we click on the update button
       (Update record button on the update window--> should also refresh the data displayed and not only the data in the db)
    h) for deployment of the application, you can checkout a tool by qt called pyqtdeploy - PyPI as an alternative to pyinstaller

    i) Check why the update function is not working

"""

from PyQt5.QtWidgets import (QTabWidget, QApplication, QVBoxLayout,
                             QDialog, QComboBox, QLabel, QHBoxLayout)

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import sys
import os
import qdarktheme
import pandas as pd
import openpyxl  #this is necessary for exporting pandas df to excel

from ark_tab1_company_brief import Tab1
from ark_tab2_saved_records_table import Tab2


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        #self.show()

        self.style_combo_box()
        self.tab_compiler()

        # Generate Scanned Folder at start of the program
        cwd = os.getcwd() # Get current working directory to be used below

        scanDocs = 'ScannedDocs'

        if not os.path.isdir(f'{cwd}/{scanDocs}'): # check if ScannedDocs Folder exists (replace '/' with '\\' for windows)
            print('Scanned Docs Folder does not exist')
            os.makedirs(scanDocs)                  # if scan docs folder does not exist, create one
        if os.path.isdir(f'{cwd}/{scanDocs}'):     # (replace '/' with '\\' for windows)
            print('Scanned Docs folder already created')


    def tab_compiler(self):

        self.setWindowTitle('AS & Associates ARK DBMS')
        x = 100
        y = 20
        w = 800
        h = 500

        self.setGeometry(x, y, w, h)
        flag = Qt.WindowMinMaxButtonsHint
        self.setWindowFlag(flag)

        # Add Tabs
        self.vbox = QVBoxLayout()
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(Tab1(), 'Company Brief')
        self.tabWidget.addTab(Tab2(), 'Saved Records')
        self.vbox.addLayout(self.style_h_layout)
        self.vbox.addWidget(self.tabWidget)
        self.setLayout(self.vbox)

    def style_combo_box(self):

        # Style Selection Horizontal Layout
        self.style_h_layout = QHBoxLayout()

        # style selection label
        self.style_label = QLabel('Style')

        # style combobox widget
        self.style_comboBox = QComboBox()


        # add items to the combobox selection
        self.style_comboBox_list = ['Standard', 'Dark', 'Light']
        self.style_comboBox.addItems(self.style_comboBox_list)

        # add label and combobox widgets to the layout
        self.style_h_layout.addWidget(self.style_label)
        self.style_h_layout.addWidget(self.style_comboBox)


        # combobox connects with the selected_style() function based on the combobox selection
        self.style_comboBox.currentTextChanged.connect(self.selected_style)

    def selected_style(self):

        # Apply dark theme to Qt application
        self.style_selection = self.style_comboBox.currentText()

        if self.style_selection == 'Dark':
            app.setStyleSheet(qdarktheme.load_stylesheet('dark'))

        elif self.style_selection == 'Light':
            app.setStyleSheet(qdarktheme.load_stylesheet('light'))

        elif self.style_selection == 'Standard':
            app.setStyleSheet('None')


# global app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())































