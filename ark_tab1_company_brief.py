from PyQt5.QtWidgets import (QWidget, QButtonGroup, QComboBox)
import sqlite3
import os
from ark_custom_message_box_class import customMessage
from ark_stacked_filing_system_frontend_class import StackedFilingSystemFrontend
from ark_db_table_and_input_class import DB_Table_Input
from ark_main_ui_class import MainUI


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        # Database credentials/parameters
        self.databaseName = 'ark_db'
        self.databaseName = f'{self.databaseName}.db'
        self.tableName = 'ark_table'

        # Connect with Database & create a table
        DB_Table_Input.connectDB(self)
        DB_Table_Input.createTable(self)

        # MainUI.boxSetup(self)
        MainUI.uiSetup(self)





    def submitRecordsButton(self):

        self.dataClean()
        try:
            # check if File No is unique
            self.checkDuplicateFileNo()
            if self.check_if_file_no_not_duplicate == "File No is unique":

                # check if File No inputs are missing
                if self.FileNo != "" :

                    # check if Company Name inputs are missing
                    if self.CoName != "":

                        # check if File No inputs pass all validations under the dataClean() function
                        if self.file_no_validated == 'Validated':
                            print('File No validated')

                            # check if Company name is unique
                            self.checkDuplicateCoName()
                            if self.check_if_co_name_not_duplicate == 'Validated':
                                print('Company Name is unique')

                                # check if Company Incorporated Dates have been changed
                                try:
                                    if self.check_if_incorporated_date_changed == "Incorporated Date Changed":
                                        print('Date Changed validated')

                                        #####################################
                                        # company status radio button
                                        try:
                                            self.statusRadioButtonClicked()
                                            if self.CoStatus:

                                                # Final check point, if all pass up to here, we proceed with generating folders and updating the database with input values
                                                self.generateFolders()
                                                self.dataUploadtoDataBase()
                                                print('Status button working')
                                            else:
                                                customMessage("Status button not checked")
                                        except:
                                            customMessage("Status button not checked")
                                        #####################################
                                    else:
                                        print("Did you forget to add the Date of Incorporation")
                                except:
                                    customMessage("Please input the Date of Incorporation")
                            else:
                                customMessage(f"{self.CoName} company name already exists in saved records, please check before proceeding")
                        else:
                            customMessage('File No inputs do not fit the required criteria, please check before proceeding')
                    else:
                        customMessage("Company Name inputs are missing")
                else:
                    customMessage("File No inputs are missing")

            else:
                customMessage(f"File No: {self.FileNo} already exist, please check before proceeding")
        except:
            print("Unable to proceed, there are inputs that do not fit the validation criteria, please check before proceeding")

    def deleteAllRecords(self):
        """ This clears all records in the current table"""

        self.c.execute(f'DELETE FROM {self.tableName}')
        self.conn.commit()

    def generateFolders(self):
        """ This function is currently called under the Submit Records folder. This was originally designed as a button that calls the function to create all of the following
        folders; Scanned Folder, Company Folders and Company Subfolders/ Respective
        47 file folders """

        cwd = os.getcwd()  # Get current working directory to be used below

        scanDocs = 'ScannedDocs'
        CompanyName = self.CoName
        docFolderList = ['Directors_Circular', 'Members_Meeting', 'Register', 'Share_Certificate', 'Summary',
                         'Checklist', 'Correspondence', 'Bill_SOA', 'SSM_Receipt', 'Application_Of_Reg',
                         'Availability_Names_Reg', 'Application_Change_Name', 'Lodgement_Constitution',
                         'Notify_Alteration_Amendment', 'Change_Reg_Add', 'Not_at_Reg_Add', 'Change_Add_Reg_Are_Kept',
                         'Change_Reg_of_Members', 'Change_Reg_Dir_Mgr_Sec', 'Annual_Return_of_Company',
                         'Approval_for_Allotment', 'Return_for_Allotment', 'Variation_Class_of_Rights',
                         'Instrument_of_Transfer', 'Solvency_Statement', 'Declaration_Appnt_as_Director',
                         'Notice_Contract_Serv_Director', 'Declaration_Appnt_as_Secretary', 'Vacate_Office_of_Secretary',
                         'Dec_by_Sec_to_Cease_Off', 'Reg_to_Act_as_Sec', 'Diff_Accounting_Periods', 'EOT_Financial_Statements',
                         'Exempt_Private_Company', 'Lodge_with_Charge', 'Series_of_Debentures', 'Assignment_of_Charge',
                         'Variations_Terms_of_Change', 'Property_Undertaking_Memo', 'Memo_Satisfaction_Reg_Charge',
                         'Dec_Verifying_Memo', 'Satisfaction_of_Charge', 'Strike_of_Company', 'Object_Striking_of_Company',
                         'Withdraw_Striking_of_Company', 'Change_in_Bus_Add_or_Nat_of_Bus', 'File_47', 'Temporary_Folder']



        if not os.path.isdir(f'{cwd}/{scanDocs}'):  # check if Scan Folder exists
            print('Scanned Docs Folder does not exists')
            os.mkdir(scanDocs)  # if does not exist create Scan Folder
            if not os.path.isdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder'):  # Check if Company Folder exist
                print(f'{CompanyName} Company Main Folder does not exists')
                os.mkdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder')  # if doesn't exist, create company folder
                print(f'Created {CompanyName} Company Main Folder')

                if not os.path.isdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder/_Folder_1'):  # check if scannedCompanyDocFolders exist
                    print(f'{CompanyName} Company SubFolders Don\'t Exist')
                    # For Loop
                    for folder in docFolderList:
                        os.mkdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder/{CompanyName}_{folder}')

                    print(f'{CompanyName} Company SubFolders Created')
                else:
                    print(f'{CompanyName} Company SubFolders Already Exist')

            else:
                print(f'{CompanyName} Company Main Folder exists')  # if main folder and company folder exist than exit


        else:  # if main folder already exist than move on
            print('Scanned Docs Folder Already Exists')
            if not os.path.isdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder'):  # if company folder doesn't exist
                os.mkdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder')  # create company folder
                print(f'Created {CompanyName} Company Main Folder')

                if not os.path.isdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder/_Folder_1'):  # check if scannedCompanyDocFolders exist
                    print(f'{CompanyName} Company SubFolders Don\'t Exist')
                    # For Loop
                    for folder in docFolderList:
                        os.mkdir(f'{cwd}/{scanDocs}/{CompanyName}_DocFolder/{CompanyName}_{folder}')
                    print(f'{CompanyName} Company SubFolders Created')
                else:
                    print(f'{CompanyName} Company SubFolders Already Exist')

            else:
                print(f'{CompanyName} Company Main Folder exists')  # if company folder exist, do nothing and exit

            print(f'List of current Directory: {os.listdir(scanDocs)}')

    def checkDuplicateCoName(self):
        """ This function checks for duplicates entries to the
        Company LineEdit and if there are no duplicates, it proceeds to
         update the db with the new record"""

        try:
            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()

            self.query = (f""" SELECT CoName FROM {self.tableName} WHERE CoName = '{self.CoName}' """)
            self.c.execute(self.query)
            self.dbCoName = self.c.execute(self.query)
            self.dbCoName = self.dbCoName.fetchone()

            if self.dbCoName:
                customMessage(f"The company {self.CoName} already exist, please check.")
            else:
                self.check_if_co_name_not_duplicate = "Validated"
        except:
            print("Unable to proceed, there is an error with the checkDuplicateCoName")

    def checkDuplicateFileNo(self):
        """ This function checks for duplicates entries to the
        Company LineEdit and if there are no duplicates, it proceeds to
         update the db with the new record"""

        try:
            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()

            self.query = (f""" SELECT FileNo FROM {self.tableName} WHERE FileNo = '{self.FileNo}' """)
            self.c.execute(self.query)
            self.dbFileNo = self.c.execute(self.query)
            self.dbFileNo = self.dbFileNo.fetchone()



            if self.dbFileNo:
                self.check_if_file_no_not_duplicate = "File No is NOT Unique"
            else:
                self.check_if_file_no_not_duplicate = "File No is unique"
        except:
            print("Unable to proceed, there is an error with the checkDuplicateFileNo")

    def openFilingSystemButton(self):
        """ When this button is clicked, a new instance of the Filing System
        is opened in a new window """


        """ Now when this button is clicked, a new instance of the Filing System
        is opened in a new window, this is different form the above in that this now
        opens a new instance of the stackedwidget filing system (stackedFilingSystem_v2_forloop)"""

        self.filingSystem = StackedFilingSystemFrontend()
        self.filingSystem.show()

    def incorporatedDateChanged(self):
        """ takes signal from dateFiled() and QDateEdit within dateFIled() and converts to text
        which is then used by the fileCopy() to validate if date has been changed
        before proceeding."""
        print('Date Changed')
        self.check_if_incorporated_date_changed = "Incorporated Date Changed"
        # self.dateEditIncorporatedDateChecked = self.dateEditIncorporatedDate.text()
        # return self.dateEditIncorporatedDateChecked

    def dataClean(self):


        try:
            self.FileNo = self.lineEdit_3_FileNo.text()

            try:

                if self.FileNo.isalpha():
                    print('File No cannot be alphabets')
                    self.file_no_validated = 'Not Validated'

                elif self.FileNo.isalpha():
                    print('File No cannot be alphabets')
                    self.file_no_validated = 'Not Validated'

                elif self.FileNo == '000':
                    print('File No cannot be 000')
                    self.file_no_validated = 'Not Validated'

                elif self.FileNo == 000:
                    print('File No cannot be 000')
                    self.file_no_validated = 'Not Validated'

                elif self.FileNo == '':
                    print('FileNo is missing an input')
                    self.file_no_validated = 'Not Validated'

                elif len(str(self.FileNo)) < 3:
                    print(len(str(self.file_no)))
                    print('File No needs to have 3 whole numbers')
                    self.file_no_validated = 'Not Validated'

                elif len(str(self.FileNo)) > 3:
                    print('File No needs to have 3 whole numbers')
                    self.file_no_validated = 'Not Validated'
                else:
                    self.file_no_validated = 'Validated'
            except:
                print('File No needs to have 3 whole numbers')
        except:
            print('Error with File No input')

        self.FileNo = self.lineEdit_3_FileNo.text()

        self.CoName = self.lineEdit_coName.text()
        self.CoName = self.CoName.strip()
        self.CoName = self.CoName.title()

        self.CoOldName = self.lineEdit_coOldName.text()
        self.RegNO = self.lineEdit_regNo.text()

        self.DateOfChange = self.dateEditDateOfChange.text()
        self.IncDate = self.dateEditIncorporatedDate.text()

        self.RegisteredAdd = self.lineRegisteredAdd.toPlainText()
        self.BusinessAdd = self.lineBusinessAdd.toPlainText()
        self.NatureOfBusiness = self.lineEditNatureOfBusiness.text()
        self.PaidUpCapital = self.lineEditPaidUpCapital.text()
        self.Member1 = self.editMembers_1.text()
        self.Member1_Shares = self.lineEditShares_1.text()
        self.Member2 = self.editMembers_2.text()
        self.Member2_Shares = self.lineEditShares_2.text()
        self.Member3 = self.editMembers_3.text()
        self.Member3_Shares = self.lineEditShares_3.text()
        self.Member4 = self.editMembers_4.text()
        self.Member4_Shares = self.lineEditShares_4.text()
        self.Member5 = self.editMembers_5.text()
        self.Member5_Shares = self.lineEditShares_5.text()

        self.Director1 = self.lineEditDirectorName_1.text()
        self.Director2 = self.lineEditDirectorName_2.text()
        self.Director3 = self.lineEditDirectorName_3.text()
        self.Director4 = self.lineEditDirectorName_4.text()
        self.Director5 = self.lineEditDirectorName_5.text()
        #------------------------------------------------------------------------------------------------------------
        self.Secretaries1 = self.lineEditSecretariesName_1.text()
        self.Secretaries1AppointedDate = self.dateEditAppointedDate_Secretary_1.text()
        self.Secretaries1ResignedDate = self.dateEditResignedDate_Secretary_1.text()
        self.Secretaries1VacatedDate = self.dateEditVacatedDate_Secretary_1.text()

        self.Secretaries2 = self.lineEditSecretariesName_2.text()
        self.Secretaries2AppointedDate = self.dateEditAppointedDate_Secretary_2.text()
        self.Secretaries2ResignedDate = self.dateEditResignedDate_Secretary_2.text()
        self.Secretaries2VacatedDate = self.dateEditVacatedDate_Secretary_2.text()

        #------------------------------------------------------------------------------------------------------------
        self.ContactPerson = self.lineEditContactPerson.text()
        self.ContactPersonTel = self.lineEditContactTel.text()
        self.ContactPersonEmail = self.lineEditContactEmail.text()

        self.PreparedBy = self.lineEditPreparedBy.text()
        self.PreparedDate = self.dateEditPrepared.text()
        self.ScannedBy = self.lineEditScannedBy.text()
        self.ScannedDate = self.dateEditScanned.text()
        self.CheckedBy = self.lineEditCheckedBy.text()
        self.CheckedDate = self.dateEditChecked.text()

    def statusRadioButtonClicked(self):
        if self.statusRadioButton_1.isChecked():
            self.CoStatus = self.statusRadioButton_1.text()
            print(self.CoStatus)

        elif self.statusRadioButton_2.isChecked():
            self.CoStatus = self.statusRadioButton_2.text()
            print(self.CoStatus)
        elif self.statusRadioButton_3.isChecked():
            self.CoStatus = self.statusRadioButton_3.text()
            print(self.CoStatus)
        else:
            print("Status_radio button not checked, we are unable to proceed")

    def dataUploadtoDataBase(self):

        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()

        self.c.execute(f"INSERT INTO {self.tableName} ({self.field1}, {self.field2},{self.field3} ,{self.field4},"
                       f"{self.field5} ,{self.field6} ,{self.field7} ,{self.field8} ,{self.field9} ,{self.field10},"
                       f"{self.field11},{self.field12},{self.field13},{self.field14},{self.field15},{self.field16},"
                       f"{self.field17},{self.field18},{self.field19},{self.field20}, {self.field21},{self.field22},"
                       f"{self.field23},{self.field24},{self.field25},{self.field26},{self.field27},{self.field28},"
                       f"{self.field29},{self.field30},{self.field31},{self.field32},{self.field33},{self.field34},"
                       f"{self.field35},{self.field36},{self.field37},{self.field38},{self.field39},"
                       f"{self.field40}, {self.field41}, {self.field42}, {self.field43}) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, "
                       f"?, ?, ?, ?, ?, ?,"
                       f" ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (self.FileNo, self.CoName, self.CoOldName, self.RegNO, self.DateOfChange,
                        self.IncDate, self.CoStatus, self.RegisteredAdd, self.BusinessAdd,
                        self.NatureOfBusiness, self.PaidUpCapital, self.Member1, self.Member1_Shares,
                        self.Member2, self.Member2_Shares, self.Member3, self.Member3_Shares,
                        self.Member4, self.Member4_Shares, self.Member5, self.Member5_Shares,
                        self.Director1, self.Director2, self.Director3, self.Director4, self.Director5,
                        self.Secretaries1, self.Secretaries1AppointedDate,
                        self.Secretaries1ResignedDate, self.Secretaries1VacatedDate, self.Secretaries2,
                        self.Secretaries2AppointedDate, self.Secretaries2ResignedDate, self.Secretaries2VacatedDate,
                        self.ContactPerson, self.ContactPersonTel, self.ContactPersonEmail,
                        self.PreparedBy, self.PreparedDate, self.ScannedBy, self.ScannedDate, self.CheckedBy,
                        self.CheckedDate))

        self.conn.commit()
        print(f'Database Updated with {self.CoName}')
        self.openFilingSystemButton()