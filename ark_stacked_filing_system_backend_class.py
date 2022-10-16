from PyQt5.QtWidgets import (QListWidget, QWidget, QPushButton, QDateEdit,
                             QVBoxLayout, QHBoxLayout, QListWidgetItem,
                             QComboBox, QLabel)

from PyQt5.QtCore import *
import os
import shutil
import sqlite3
import json
from ark_custom_message_box_class import customMessage


""" Filing Window"""
""" This is for the separate window, once the Submit Record button is clicked on the Company Brief window.This window
    should be a stacked widget that switches between the 48 folders. Therefore each stacked widget represents a file
    tray that copies files to it's respective folder(one of the 48 folders. The combobox should be pulling information
    from the list of Company Folders (currently it pulls from the DB CoName field) that have been generated thus far, hence 
    the Company Name in DB = Company Folder Names = Company Names in the Filing System Combo Box ."""


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            self.links = []
            print(event.mimeData().urls())

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.links.append(str(url.toLocalFile()))
                else:
                    self.links.append(str(url.toString()))

            self.addItems(self.links)
        else:
            event.ignore()

class StackedFilingSystemBackend(QWidget):

    def __init__(self, fileFolderName):
        super().__init__()


        # Connect with Database
        self.databaseName = 'ark_db'
        self.databaseName = f'{self.databaseName}.db'
        self.tableName = 'ark_table'

        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()

        # Date Filed
        self.fileDateLabel = QLabel('Date Filed')
        self.fileDateEdit = QDateEdit()

        # date to be displayed in string format
        date_str = '1-Jan-1950'

        # convert date str to QDate
        qdate = QDate.fromString(date_str, 'd-MMM-yyyy')

        self.fileDateEdit.setDisplayFormat('d-MMM-yyyy')
        self.fileDateEdit.setDate(qdate)


        # File Folder Name
        self.fileFolderName = f'_{fileFolderName}'

        # File Name
        self.fileName = self.fileFolderName

        # self.titleRespectiveToStackedWidget()
        self.title = QLabel(f"{fileFolderName.replace('_',' ')}")  # Title for the respective Stacked Widget, which follows the File Folder Name i.e. 'Directors Circular'
        self.title.setAlignment(Qt.AlignCenter)

        self.typeOfMeetingComboBoxSetup()
        self.selectCompanyComboBoxFunction()
        self.fileTray()
        self.buttons()
        self.backendLayoutSetup()
        self.dateFiled()



    def titleRespectiveToStackedWidget(self):
        """This function is to covert the File Folder name generated
        as the Filing System instance constructor to the Stacked Window respective title
        i.e. 'Directors_Circular ---> Directors Circular Folder """

        title1 = self.fileFolderName.split('_')[0]
        title2 = self.fileFolderName.split('_')[1]
        self.title = f'{title1} {title2} Folder'
        return self.title

    def dateFiled(self):
        """ sets up date label, date widget, and also checks if date has been changed. When changed,
        a signal connects to dateChanged() function to call out the date in text format. This date
        in text format is then used by the fileCopy() function which uses an if statement to check
        if date has been changed or else would not let you move to the next step."""

        self.hdateLayout.addWidget(self.fileDateLabel)
        self.hdateLayout.addWidget(self.fileDateEdit)
        self.fileDateEdit.dateChanged.connect(self.dateChanged)

    def dateChanged(self):
        """ takes signal from dateFiled() and QDateEdit within dateFIled() and converts to text
        which is then used by the fileCopy() to validate if date has been changed
        before proceeding."""
        self.date = self.fileDateEdit.text()
        return self.date

    def selectCompanyComboBoxFunction(self):
        """ this connects to the db and pulls the records from the CoName field
        which is used to populate the ComboBox list. You will see a for loop below
        that is used to populate the db query into a list which is then used by the ComboBox."""

        # Database connect and query table for combobox company list
        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()
        self.query = f"SELECT CoName FROM {self.tableName}"
        self.c.execute(self.query)
        self.selectCompanyComboBox = self.c.execute(
            self.query)  # This is purely Python, not PyQt, the ComboBox is only set up at below using the same name

        self.selectCompanyComboBoxList = []  # Python List that used to add items to the searchComboBox (This is Python not PyQt)
        for company in self.selectCompanyComboBox:
            self.selectCompanyComboBoxList.append(company[0])
            self.combo_box_list_company = company[0]

        # ComboBox Setup
        self.labelSelectCompanyComboBox = QLabel('Search Company')
        self.selectCompanyComboBox = QComboBox()
        self.selectCompanyComboBox.addItems(self.selectCompanyComboBoxList)  # items from the CoName in db are added to the searchComboBox from a Python List
        self.company = self.selectCompanyComboBox.currentText()

        # ComboBox Layout

        """Additional Notes: There are two parts here, one is the db, db query, and the for loop that gets the 
        db content and then stores in a list. All this is python, and done before the Qt.ComboBox is set up. So maybe we 
        can break them apart to make it more transferable."""

    def fileTray(self):
        """ sets up the ListWidget for the file tray and
        retrieves the text of the current selected item in the list widget"""

        # ListWidget 1
        self.label_FileTray1 = QLabel('Directors Circular')
        self.listWidget_FileTray1 = ListBoxWidget()
        self.item_FileTray1 = QListWidgetItem(self.listWidget_FileTray1.currentItem())
        self.item_FileTray1 = self.item_FileTray1.text()

    def buttons(self):
        # PushButton
        self.clearListButton = QPushButton('Clear List')
        self.clearListButton.clicked.connect(self.clearList)
        self.fileCopyButton = QPushButton('Copy File (File must be highlighted)')
        self.fileCopyButton.clicked.connect(self.fileCopy)


    def clearList(self):
        """ Clears all from the list, ListWidget does not have clear
        selected item. Need to stop more than one file drop! But
        I am coming to find out that there might be a way to clear
        each selected item one at a time"""

        try:
            self.selectedItemToBeCleared = self.listWidget_FileTray1.currentItem()
            self.listWidget_FileTray1.clear()
        except:
            customMessage('Unable to clear list, check the clearSelectedListItem method')

    def fileCopy(self):
        """ Folder & File Hierarchy: ScannedDocs/CompanyFolder/CompanyFileNameFolder/CompanyFileName.pdf
         i.e. CompanyFolder = Tesla, CompanyFileNameFolder = Tesla_Directors_Circular, CompanyFileName = date_Tesla_directors_circular_1"""

        """The largest method in this class. Copies the selected file dropped
        into the listwidget/filetray to the respective folder, in this order:
        ScannedDocs/Company/CompanyDoc/File.
        The file will be using a formatted date at the beginning of the filename
        which the user would need to select before saving/copying the file."""

        """Checks if the date has been changed"""

        print(self.title)

        try:
            print(self.date)
        except:
            customMessage('Did you forget to set the date?')

        try:

            """Retrieves the number of files dropped into the file tray, 
            this count is then used to prevent either trying to save
            with 0 or more than 1 file dropped"""

            self.listWidget_FileTray1Count = self.listWidget_FileTray1.count()
            print(f'No of file: {self.listWidget_FileTray1Count}')

            if self.listWidget_FileTray1Count == 1:

                """" Gets the text of the selected item in the listwidget,
                 this will be used as the source file that is to be copied.
                 Not really sure if we need to do this"""

                self.item_FileTray1 = QListWidgetItem(self.listWidget_FileTray1.currentItem())
                self.item_FileTray1 = self.item_FileTray1.text()

                """Retrieves the name selected on the ComboBoxList, 
                which is used as the Company Name for Company Folder"""

                self.comboBoxCoNameSelection = self.selectCompanyComboBox.currentText()
                self.companyFolderName = f'{self.comboBoxCoNameSelection}_DocFolder'

                """Variable for the SubFolder one level below the Company Folder,
                 will have 48 of these which is 47 plus 1 Miscellaneous"""

                """Variable for file name extension for all those in the Directors Circular Folder"""

                # File Date (Each File is supposed to have a date associated to it)
                date = self.date
                date1 = date.split('-')[0]
                date2 = date.split('-')[1]
                date3 = date.split('-')[2]
                self.directorsCircularFileDate = f'{date1}_{date2}_{date3}_'


                self.directorsCircularFolderPath = f'ScannedDocs/{self.companyFolderName}/{self.comboBoxCoNameSelection}{self.fileFolderName}'
                self.directorsCircularFolderFileCount = len(os.listdir(self.directorsCircularFolderPath))

                # Destination directory

                try:
                    self.type_of_meeting_combobox_validation_function() # function validates if the right Type of Meeting has been selected for the appropriate folder
                                                                        # (Only the Directors and Members Meeting folders require a type of meeting being selected,
                                                                        #  and there are 3 types for each, Directors Circular and Members Meeting folders)

                except:
                    customMessage('Type of meeting validation did not pass')


                self.savedFilePathLink()
                self.fileFolderListFunction()
                self.uploadFileFolderList()
                self.listWidget_FileTray1.clear()


            elif self.listWidget_FileTray1Count == 0:
                customMessage('There are no files to be copied, you need to drop a file.')

            elif self.listWidget_FileTray1Count > 1:  # Please test this code, it was == 0 previously
                customMessage('You have more than one file, you can only copy one file at a time.')

        except:
            customMessage('Unable to save file, kindly check your code under the try accept block for fileCopy()')

    def savedFilePathLink(self):
        try:
            print(self.newDirectory)
        except:
            print('Cannot print saved file path')

    def fileFolderListFunction(self):
        try:
            self.fileFolderList = os.listdir(f'ScannedDocs/{self.companyFolderName}/{self.comboBoxCoNameSelection}'
                                             f'{self.fileFolderName}')
            # print(f'FileFolderList: self.fileFolderList:: {self.fileFolderList}')
        except:
            print('Unable to print Directory Listing for Folder')

    def uploadFileFolderList(self):

        # print(f'self.tableName: {self.tableName}')
        # print(f'File Folder Name:{self.fileFolderName}')
        self.fileFolderListFieldName = self.fileFolderName
        # print(f'File Folder List Field Name: {self.fileFolderListFieldName}')
        # print(f'self.comboBoxCoNameSelection: {self.comboBoxCoNameSelection}')
        # print(f'self.fileFolderList: {self.fileFolderList}')

        self.listjSon = json.dumps(self.fileFolderList)

        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()

        # print("Test Line 310")

        try:
            self.c.execute(f"""UPDATE {self.tableName} SET {self.fileFolderListFieldName} =
             '{self.listjSon}' WHERE CoName='{self.comboBoxCoNameSelection}' """)

            customMessage(f"DataBase successfully updated with {self.comboBoxCoNameSelection}'s"
                  f" {self.fileFolderListFieldName} folder file lists.")

            # print(f'Self.ListJSON: {self.listjSon}')

        except:

            customMessage(f'Unable to update DB with File Folder List for Company: '
                  f'{self.comboBoxCoNameSelection}\'s {self.fileFolderListFieldName} folder.')

        self.conn.commit()

    def typeOfMeetingComboBoxFunction(self):
        """ this is a combobox for user to select types of meeting associated only with the
            Directors Circular and Members Meeting Folders, there are 6 options in total
            3 each, which are: BOD, MM, AGM, EGM, xxx, xxx
            This options are to be included in the filed name
            This functions is associated with the setup of the combobox function named:
            typeOfMeetingComboBoxSetup()
        """

        try:
            typeOfMeetingComboBoxSelection = self.typeOfMeetingComboBox.currentText()

            # Need to insert if DC or MM folder and if typeOfMeeting !='':
            if typeOfMeetingComboBoxSelection != '':
                print(f'Type of Meeting: {typeOfMeetingComboBoxSelection}')

            else:
                print('You have not made a selection from the Stacked Combo Box')
        except:
            print('Not printing Combo Box Selection from Stacked Widget, check stackedComboBoxSelectionFunction')

        try:
            if self.fileFolderName == '_Directors_Circular' or self.fileFolderName == '_Members_Meeting':
                print(f'Testing if Directors Folder or Members Meeting: {typeOfMeetingComboBoxSelection}')
        except:
            print('Line 343: Type of Meeting ComboBox Function not printing if Directors Folder')

    def typeOfMeetingComboBoxSetup(self):
        """ this is a combobox for user to select types of meeting associated only with the
            Directors Circular and Members Meeting Folders, there are 6 options in total
            3 each, which are: BOD, MM, AGM, EGM, xxx, xxx
            This options are to be included in the file name
            This function is associated with the functioning version of the combobox function
            named: typeOfMeetingComboBoxFunction()
        """


        typeOfMeetingComboBoxItems = ['', 'BOD', 'DR', 'DWR', 'AGM', 'EGM', 'MWR']

        self.typeOfMeetingComboBoxLabel = QLabel('Select Type of Meeting')
        self.typeOfMeetingComboBox = QComboBox()
        self.typeOfMeetingComboBox.addItems(typeOfMeetingComboBoxItems)
        # self.typeOfMeetingComboBox.currentTextChanged.connect(self.typeOfMeetingComboBoxFunction)

    def backendLayoutSetup(self):
        """Setup for all the layouts in this class"""

        # File Folder Name
        # print(f'Layout: {self.fileFolderName}')

        # Layout

        # Combo Box for Directors Circular and Members Meeting selection
        self.typeOfMeetingComboBoxHBoxLayout = QHBoxLayout()
        self.typeOfMeetingComboBoxHBoxLayout.addWidget(self.typeOfMeetingComboBoxLabel)
        self.typeOfMeetingComboBoxHBoxLayout.addWidget(self.typeOfMeetingComboBox)

        # Main Layout
        self.mainLayoutTab2 = QVBoxLayout()

        # Stacked Widget Title
        self.htitleLabelLayout = QHBoxLayout()
        self.htitleLabelLayout.addWidget(self.title)
        self.mainLayoutTab2.addLayout(self.htitleLabelLayout)

        # Combo Box for Directors Circular and Members Meeting selection

        # Date Filed Layout
        self.hdateLayout = QHBoxLayout()
        self.mainLayoutTab2.addSpacing(10)

        # ComboBox Layout
        self.hlayoutSelectCompanyComboBox = QHBoxLayout()
        self.hlayoutSelectCompanyComboBox.addWidget(self.labelSelectCompanyComboBox)
        self.hlayoutSelectCompanyComboBox.addWidget(self.selectCompanyComboBox)

        self.mainLayoutTab2.addLayout(self.hlayoutSelectCompanyComboBox)  # You remove this, the searchComboBox will fail, you will not be able to get the selected Company name item
        self.mainLayoutTab2.addSpacing(20)
        self.mainLayoutTab2.addLayout(self.hdateLayout)
        self.mainLayoutTab2.addLayout(self.typeOfMeetingComboBoxHBoxLayout)
        self.mainLayoutTab2.addSpacing(10)  # spacing between meeting combobox and file drop window
        self.mainLayoutTab2.addWidget(self.listWidget_FileTray1)

        self.mainLayoutTab2.addWidget(self.fileCopyButton)
        self.mainLayoutTab2.addWidget(self.clearListButton)
        self.setLayout(self.mainLayoutTab2)

    def type_of_meeting_combobox_validation_function(self):

        """ This function will choose the list of items in the meeting type combobox based on
            whether it is Directors Circular(DC_1, DC_2, DC_3) or Members Meeting (MM_1, MM_2, MM_3)
        """

        # Text formatting to replace '_' with ' '
        # self.fileName = self.fileName[1:]
        # self.fileName = self.fileName.replace('_',' ')

        # # Text formatting to replace '_' with ' '
        # self.fileFolderName = self.fileFolderName[1:]
        # self.fileFolderName = self.fileFolderName.replace('_', ' ')

        try:

            if self.fileFolderName != '_Directors_Circular' and self.fileFolderName != '_Members_Meeting':
                if self.typeOfMeetingComboBox.currentText() != '':
                    customMessage('You cannot select any Type of Meeting to save to this folder')

            if self.fileFolderName != '_Directors_Circular' and self.fileFolderName != '_Members_Meeting' and self.typeOfMeetingComboBox.currentText() == '':
                self.newDirectory = f'ScannedDocs/{self.companyFolderName}/{self.comboBoxCoNameSelection}{self.fileFolderName}/{self.directorsCircularFileDate}{self.fileName}_{self.directorsCircularFolderFileCount + 1}.pdf'
                shutil.copyfile(self.item_FileTray1, self.newDirectory)
                customMessage(f'{self.fileName} dated {self.directorsCircularFileDate} has been successfully saved to {self.fileFolderName} in {self.comboBoxCoNameSelection} folder')

            if self.fileFolderName == '_Members_Meeting' and self.typeOfMeetingComboBox.currentText() == '':
                customMessage('You need to select the appropriate Type of Meeting to save to this folder')

            if self.fileFolderName == '_Directors_Circular':
                if self.typeOfMeetingComboBox.currentText() == '':
                    customMessage('You need to select the appropriate Type of Meeting to save to this folder')

                if self.typeOfMeetingComboBox.currentText() == 'AGM' or self.typeOfMeetingComboBox.currentText() == 'EGM' or self.typeOfMeetingComboBox.currentText() == 'MWR':
                    customMessage('You cannot select the current Type of Meeting for this folder')

                elif self.typeOfMeetingComboBox.currentText() == 'BOD' or self.typeOfMeetingComboBox.currentText() == 'DR' or self.typeOfMeetingComboBox.currentText() == 'DWR':
                    self.newDirectory = f'ScannedDocs/{self.companyFolderName}/{self.comboBoxCoNameSelection}{self.fileFolderName}/{self.directorsCircularFileDate}{self.fileName}_{self.typeOfMeetingComboBox.currentText()}_{self.directorsCircularFolderFileCount + 1}.pdf'
                    shutil.copyfile(self.item_FileTray1, self.newDirectory)
                    customMessage(f'{self.fileName} dated {self.directorsCircularFileDate} has been successfully saved to {self.fileFolderName} in {self.comboBoxCoNameSelection} folder')

            if self.fileFolderName == '_Members_Meeting':
                if self.typeOfMeetingComboBox.currentText() == '':
                    customMessage('You need to select the appropriate Type of Meeting to save to this folder')

                if self.typeOfMeetingComboBox.currentText() == 'BOD' or self.typeOfMeetingComboBox.currentText() == 'DR' or self.typeOfMeetingComboBox.currentText() == 'DWR':
                    customMessage('You cannot select the current Type of Meeting for this folder')

                elif self.typeOfMeetingComboBox.currentText() == 'AGM' or self.typeOfMeetingComboBox.currentText() == 'EGM' or self.typeOfMeetingComboBox.currentText() == 'MWR':
                    self.newDirectory = f'ScannedDocs/{self.companyFolderName}/{self.comboBoxCoNameSelection}{self.fileFolderName}/{self.directorsCircularFileDate}{self.fileName}_{self.typeOfMeetingComboBox.currentText()}_{self.directorsCircularFolderFileCount + 1}.pdf'
                    shutil.copyfile(self.item_FileTray1, self.newDirectory)
                    customMessage(f'{self.fileName} dated {self.directorsCircularFileDate} has been successfully saved to {self.fileFolderName} in {self.comboBoxCoNameSelection} folder')


        except:
                print('The Type of Meeting ComboBox Validation is not working')




























