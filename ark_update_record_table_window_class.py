from PyQt5.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QDateEdit, QTextEdit,
                             QVBoxLayout, QLineEdit, QWidget, QScrollArea, QComboBox, QMessageBox)

from PyQt5.QtCore import Qt, QDate
from ark_custom_message_box_class import customMessage

import sqlite3


class UpdateWindow(QWidget):  # Name here has been changed to MainWindow2
    def __init__(self, selectedRowToDeepView):
        super().__init__()
        x = 100
        y = 630
        w = 900
        h = 400

        self.setWindowTitle('Update Record View')
        self.setGeometry(x, y, w, h)
        self.setMaximumWidth(w)
        flag = Qt.WindowMinMaxButtonsHint
        self.setWindowFlag(flag)

        # Database
        self.databaseName = 'ark_db'
        self.databaseName = f'{self.databaseName}.db'
        self.tableName = 'ark_table'

        self.selectedRow1 = selectedRowToDeepView

        self.comboBoxCompanyList()
        self.uiSetup_UpdateView()
        self.setComboBoxToFirstCoName()

    def uiSetup_UpdateView(self):
        # File No

        # ComboBox Layout for Company Selection in DeepView Mode

        self.comboBoxLabel = QLabel('Please select a company you would like to update')
        self.comboHBoxLayout = QHBoxLayout()
        self.comboVBoxLayout = QVBoxLayout()
        self.comboBoxDeepView = QComboBox()
        self.comboBoxDeepView.addItems(self.comboBoxList)
        self.ifComboBoxItemSelected()  # This signals when combobox item has been selected

        self.comboBoxDeepView.setMaximumWidth(200)
        self.comboVBoxLayout.addWidget(self.comboBoxLabel)
        self.comboVBoxLayout.addWidget(self.comboBoxDeepView)
        self.comboHBoxLayout.addLayout(self.comboVBoxLayout)

        # Horizontal Layout 1

        self.horizontalLayout_1 = QHBoxLayout()
        self.label_fileNo = QLabel('File No')
        self.horizontalLayout_1.addWidget(self.label_fileNo)
        self.lineEdit_3_FileNo = QLineEdit()
        self.lineEdit_3_FileNo.setReadOnly(True)

        # File NO Input
        self.lineEdit_3_FileNo.setText(self.selectedRow1[0])  # <-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_3_FileNo)

        self.label_name = QLabel('Company Name')
        self.horizontalLayout_1.addWidget(self.label_name)
        self.lineEdit_coName = QLineEdit()
        self.lineEdit_coName.setText(self.selectedRow1[1])  # <-------------------------------------------
        self.lineEdit_coName.setReadOnly(True)  # <-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_coName)

        self.label_oldName = QLabel('Old Name')
        self.horizontalLayout_1.addWidget(self.label_oldName)
        self.lineEdit_coOldName = QLineEdit()
        self.lineEdit_coOldName.setText(self.selectedRow1[2])  # <-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_coOldName)

        self.label_regNo = QLabel('Reg No')
        self.horizontalLayout_1.addWidget(self.label_regNo)
        self.lineEdit_regNo = QLineEdit()
        self.lineEdit_regNo.setText(self.selectedRow1[3])  # <-------------------------------------------
        self.horizontalLayout_1.addWidget(self.lineEdit_regNo)

        # Horizontal Line 2 Date of Change ############################################################################################################
        self.label_DateOfChange = QLabel('Date Of Change')

        self.newDateEditDateOfChange = self.selectedRow1[4]  # <-------------------------------------------
        self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")

        self.dateEditDateOfChange = QDateEdit()
        self.dateEditDateOfChange.setDisplayFormat("d-MMM-yyyy")
        self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)

        # https://www.geeksforgeeks.org/pyqt5-qdateedit-date-changed-signal/
        # Need to check if date is changed and if not need to put out a message or else set date to something obvious as unusable

        # Horizontal Line 2 : Date Incorporated
        self.label_IncorporatedDate = QLabel('Incorporated Date')

        self.newDateEditIncorporatedDate = self.selectedRow1[5]
        self.setDateNewDateEditIncorporatedDateString = QDate.fromString(self.newDateEditIncorporatedDate, "d-MMM-yyyy")

        self.dateEditIncorporatedDate = QDateEdit()
        self.dateEditIncorporatedDate.setDisplayFormat(
            "d-MMM-yyyy")  # <-------------------------------------------------------- Date Incorporated
        self.dateEditIncorporatedDate.setDate(self.setDateNewDateEditIncorporatedDateString)

        # Vertical Layout for Date of Change and Incorporation
        self.dateOfChangeVerticalLayout_1 = QVBoxLayout()
        self.dateOfChangeVerticalLayout_1.addWidget(self.label_DateOfChange)
        self.dateOfChangeVerticalLayout_1.addWidget(self.dateEditDateOfChange)

        self.dateOfIncorporationVerticalLayout_1 = QVBoxLayout()
        self.dateOfIncorporationVerticalLayout_1.addWidget(self.label_IncorporatedDate)
        self.dateOfIncorporationVerticalLayout_1.addWidget(self.dateEditIncorporatedDate)

        # Vertical Layout: Type of Company
        # self.radioButtonTypeVerticalLayout_1 = QVBoxLayout()
        # self.typeLabel = QLabel('Type')
        # self.typeLabelBlank = QLabel('')  # This is used to insert blank spacing
        # #--------------------------------------------------------------------------------------Radio Buttons--------------------
        # # Radio Buttons: Type of Company
        #
        # self.typeRadioButton_1 = QRadioButton('Limited By Shares')
        # self.typeRadioButton_2 = QRadioButton('Private Limited')
        #
        # if self.selectedRow1[6] == 'Limited By Shares':
        #     self.typeRadioButton_1.setChecked(True)
        # elif self.selectedRow1[6] == 'Private Limited':
        #     self.typeRadioButton_2.setChecked(True)
        # else:
        #     pass

        # Radio Button Group: Type of Company
        # self.radioButtonGroup_Company_Type = QButtonGroup(self)
        # self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_1)
        # self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_2)
        # <---- -------------------------------- Set typeradioButton Input from DB

        # self.radioButtonTypeVerticalLayout_1.addWidget(self.typeLabel)
        # self.radioButtonTypeVerticalLayout_1.addWidget(self.typeLabelBlank)  # Blank Spacing for better alignment of Vertical Radio Buttons
        # self.radioButtonTypeVerticalLayout_1.addWidget(self.typeRadioButton_1)
        # self.radioButtonTypeVerticalLayout_1.addWidget(self.typeRadioButton_2)

        # Vertical Layout: Status of Company
        # self.radioButtonStatusVerticalLayout_2 = QVBoxLayout()
        # self.statusLabel = QLabel('Status')
        #
        # # Radio Buttons: Status of Company
        # # self.lineEdit_3_FileNo.setText(self.selectedRow1[0])
        #
        # self.statusRadioButton_1 = QRadioButton('Existing')
        # self.statusRadioButton_2 = QRadioButton('Dissolved')
        # self.statusRadioButton_3 = QRadioButton('Winding Up')
        #
        # if self.selectedRow1[6] == 'Existing':
        #     self.statusRadioButton_1.setChecked(True)
        #
        # elif self.selectedRow1[6] == 'Dissolved':
        #     self.statusRadioButton_2.setChecked(True)
        # elif self.selectedRow1[6] == 'Winding Up':
        #     self.statusRadioButton_3.setChecked(True)
        # else:
        #     pass
        #                                                                                 # <------------- Set typeradioButton Input from DB

        # Radio Button Group: Status of Company
        # self.radioButtonGroup_Company_Status = QButtonGroup(self)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_1)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_2)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_3)
        #
        # self.radioButtonStatusVerticalLayout_2.addWidget(self.statusLabel)
        # self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_1)
        # self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_2)
        # self.radioButtonStatusVerticalLayout_2.addWidget(self.statusRadioButton_3)
        # ----------------------------------------------------------------------------------------------- Radio Buttons End---------------

        self.horizontalLayout_2 = QHBoxLayout()  # Horizontal Line 2

        self.horizontalLayout_2.addLayout(self.dateOfChangeVerticalLayout_1)
        self.horizontalLayout_2.addLayout(self.dateOfIncorporationVerticalLayout_1)
        # self.horizontalLayout_2.addLayout(self.radioButtonTypeVerticalLayout_1)
        # self.horizontalLayout_2.addLayout(self.radioButtonStatusVerticalLayout_2)

        # Horizontal Layout 3: Registered & Business Address ######################################################################################

        # Registered & Business Address
        self.labelRegisteredAdd = QLabel('Registered Address')
        self.lineRegisteredAdd = QTextEdit()
        self.lineRegisteredAdd.setText(self.selectedRow1[7])  # <-------------------------------------------
        self.lineRegisteredAdd.setFixedHeight(40)
        self.verticalLayout3_RegisteredAdd = QVBoxLayout()
        self.verticalLayout3_RegisteredAdd.addWidget(self.labelRegisteredAdd)
        self.verticalLayout3_RegisteredAdd.addWidget(self.lineRegisteredAdd)

        self.labelBusinessAdd = QLabel('Business Address')
        self.lineBusinessAdd = QTextEdit()
        self.lineBusinessAdd.setText(self.selectedRow1[8])  # <-------------------------------------------
        self.lineBusinessAdd.setFixedHeight(40)
        self.verticalLayout4_BusinessAdd = QVBoxLayout()
        self.verticalLayout4_BusinessAdd.addWidget(self.labelBusinessAdd)
        self.verticalLayout4_BusinessAdd.addWidget(self.lineBusinessAdd)

        self.horizontalLayout_3_RegBusiness_Add = QHBoxLayout()  # Business and Registered Address VBox
        self.horizontalLayout_3_RegBusiness_Add.addLayout(self.verticalLayout3_RegisteredAdd)
        self.horizontalLayout_3_RegBusiness_Add.addLayout(self.verticalLayout4_BusinessAdd)

        # Nature of Business

        self.labelNatureOfBusiness = QLabel('Nature of Business')
        self.lineEditNatureOfBusiness = QLineEdit()
        self.lineEditNatureOfBusiness.setText(self.selectedRow1[9])  # <-------------------------------------------

        self.labelPaidUpCapital = QLabel('Paid-Up Capital')
        self.lineEditPaidUpCapital = QLineEdit()
        self.lineEditPaidUpCapital.setText(self.selectedRow1[10])  # <-------------------------------------------

        self.horizontalLayout_4_NatureOfBusiness = QHBoxLayout()
        self.horizontalLayout_4_NatureOfBusiness.addWidget(self.labelNatureOfBusiness)
        self.horizontalLayout_4_NatureOfBusiness.addWidget(self.lineEditNatureOfBusiness)
        self.horizontalLayout_4_NatureOfBusiness.addWidget(self.labelPaidUpCapital)
        self.horizontalLayout_4_NatureOfBusiness.addWidget(self.lineEditPaidUpCapital)

        # Members, Shares, Directors Name, Secretaries, Contact Person, Contact Tel, Contact Email

        # self.labelRegisteredAdd = QLabel('Registered Address')
        # self.lineRegisteredAdd = QTextEdit()

        self.labelMembersShares = QLabel('Members / Shares:')
        self.editMembers_1 = QLineEdit()
        self.editMembers_1.setText(self.selectedRow1[11])  # <-------------------------------------------
        self.editMembers_2 = QLineEdit()
        self.editMembers_2.setText(self.selectedRow1[13])  # <-------------------------------------------
        self.editMembers_3 = QLineEdit()
        self.editMembers_3.setText(self.selectedRow1[15])  # <-------------------------------------------
        self.editMembers_4 = QLineEdit()
        self.editMembers_4.setText(self.selectedRow1[17])  # <-------------------------------------------
        self.editMembers_5 = QLineEdit()
        self.editMembers_5.setText(self.selectedRow1[19])  # <-------------------------------------------

        self.verticalLayout5_MemberShares = QVBoxLayout()
        self.verticalLayout5_MemberShares.addWidget(self.labelMembersShares)
        self.verticalLayout5_MemberShares.addWidget(self.editMembers_1)
        self.verticalLayout5_MemberShares.addWidget(self.editMembers_2)
        self.verticalLayout5_MemberShares.addWidget(self.editMembers_3)
        self.verticalLayout5_MemberShares.addWidget(self.editMembers_4)
        self.verticalLayout5_MemberShares.addWidget(self.editMembers_5)

        self.labelShares = QLabel('Shares:')
        self.lineEditShares_1 = QLineEdit()
        self.lineEditShares_1.setText(self.selectedRow1[12])
        self.lineEditShares_2 = QLineEdit()
        self.lineEditShares_2.setText(self.selectedRow1[14])
        self.lineEditShares_3 = QLineEdit()
        self.lineEditShares_3.setText(self.selectedRow1[16])
        self.lineEditShares_4 = QLineEdit()
        self.lineEditShares_4.setText(self.selectedRow1[18])
        self.lineEditShares_5 = QLineEdit()
        self.lineEditShares_5.setText(self.selectedRow1[20])

        self.verticalLayout6_Shares = QVBoxLayout()
        self.verticalLayout6_Shares.addWidget(self.labelShares)
        self.verticalLayout6_Shares.addWidget(self.lineEditShares_1)
        self.verticalLayout6_Shares.addWidget(self.lineEditShares_2)
        self.verticalLayout6_Shares.addWidget(self.lineEditShares_3)
        self.verticalLayout6_Shares.addWidget(self.lineEditShares_4)
        self.verticalLayout6_Shares.addWidget(self.lineEditShares_5)

        self.labelDirectorName = QLabel('Director(s) Name:')
        self.lineEditDirectorName_1 = QLineEdit()
        self.lineEditDirectorName_1.setText(self.selectedRow1[21])
        self.lineEditDirectorName_2 = QLineEdit()
        self.lineEditDirectorName_2.setText(self.selectedRow1[22])
        self.lineEditDirectorName_3 = QLineEdit()
        self.lineEditDirectorName_3.setText(self.selectedRow1[23])
        self.lineEditDirectorName_4 = QLineEdit()
        self.lineEditDirectorName_4.setText(self.selectedRow1[24])
        self.lineEditDirectorName_5 = QLineEdit()
        self.lineEditDirectorName_5.setText(self.selectedRow1[25])


        self.verticalLayout7_Directors = QVBoxLayout()
        self.verticalLayout7_Directors.addWidget(self.labelDirectorName)
        self.verticalLayout7_Directors.addWidget(self.lineEditDirectorName_1)
        self.verticalLayout7_Directors.addWidget(self.lineEditDirectorName_2)
        self.verticalLayout7_Directors.addWidget(self.lineEditDirectorName_3)
        self.verticalLayout7_Directors.addWidget(self.lineEditDirectorName_4)
        self.verticalLayout7_Directors.addWidget(self.lineEditDirectorName_5)

        # Contact Person and Details

        self.labelContactPerson = QLabel('Contact Person:')
        self.lineEditContactPerson = QLineEdit()
        self.lineEditContactPerson.setText(self.selectedRow1[34])
        self.labelContactTel = QLabel('Contact Tel:')
        self.lineEditContactTel = QLineEdit()
        self.lineEditContactTel.setText(self.selectedRow1[35])
        self.labelContactEmail = QLabel('Contact Email')
        self.lineEditContactEmail = QLineEdit()
        self.lineEditContactEmail.setText(self.selectedRow1[36])

        self.verticalLayout8_Contact = QVBoxLayout()
        self.verticalLayout8_Contact.addWidget(self.labelContactPerson)
        self.verticalLayout8_Contact.addWidget(self.lineEditContactPerson)
        self.verticalLayout8_Contact.addWidget(self.labelContactTel)
        self.verticalLayout8_Contact.addWidget(self.lineEditContactTel)
        self.verticalLayout8_Contact.addWidget(self.labelContactEmail)
        self.verticalLayout8_Contact.addWidget(self.lineEditContactEmail)

        self.horizontalLayout_5_DirectorAndContact = QHBoxLayout()
        self.horizontalLayout_5_DirectorAndContact.addLayout(self.verticalLayout5_MemberShares)
        self.horizontalLayout_5_DirectorAndContact.addLayout(self.verticalLayout6_Shares)
        self.horizontalLayout_5_DirectorAndContact.addLayout(self.verticalLayout7_Directors)
        self.horizontalLayout_5_DirectorAndContact.addLayout(self.verticalLayout8_Contact)

        # Final Horizontal Layout has 3 Sub Vertical Layouts within

        # Secretaries 1 ----------------------------------------------------------------------
        self.labelSecretaries_1_Name = QLabel('Secretaries 1:')
        self.lineEditSecretariesName_1 = QLineEdit()
        self.lineEditSecretariesName_1.setText(self.selectedRow1[26])
        # self.labelSecretaries_2_Name = QLabel('Secretaries 2:')
        # self.lineEditSecretariesName_2 = QLineEdit()

        self.labelAppointedDate_Secretary_1 = QLabel('Appointed Date')
        self.labelResignedDate_Secretary_1 = QLabel('Resigned Date')
        self.labelVacatedDate_Secretary_1 = QLabel('Vacated Date')

        self.newDateEditAppointedDate_Secretary_1 = self.selectedRow1[27]
        self.setDateNewDateEditAppointedDate_Secretary_1String = QDate.fromString(
            self.newDateEditAppointedDate_Secretary_1, "d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_1 = QDateEdit()  # <-------------------------------------------------------- Sec 1 -- 25,26,27
        self.dateEditAppointedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_1.setDate(self.setDateNewDateEditAppointedDate_Secretary_1String)

        self.newDateEditResignedDate_Secretary_1 = self.selectedRow1[28]
        self.setDateNewDateEditResignedDate_Secretary_1String = QDate.fromString(
            self.newDateEditResignedDate_Secretary_1, "d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_1 = QDateEdit()
        self.dateEditResignedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_1.setDate(self.setDateNewDateEditResignedDate_Secretary_1String)

        self.newDateEditVacatedDate_Secretary_1 = self.selectedRow1[29]
        self.setDateNewDateEditVacatedDate_Secretary_1String = QDate.fromString(self.newDateEditVacatedDate_Secretary_1,
                                                                                "d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_1 = QDateEdit()
        self.dateEditVacatedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_1.setDate(self.setDateNewDateEditVacatedDate_Secretary_1String)

        # Vertical Layouts for both Secretaries Vertical 9 & 10
        # Vertical Layout 9

        self.verticalLayout9_Secretaries_1 = QVBoxLayout()
        self.verticalLayout9_Secretaries_1.addWidget(self.labelSecretaries_1_Name)
        self.verticalLayout9_Secretaries_1.addWidget(self.lineEditSecretariesName_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.labelAppointedDate_Secretary_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.dateEditAppointedDate_Secretary_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.labelResignedDate_Secretary_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.dateEditResignedDate_Secretary_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.labelVacatedDate_Secretary_1)
        self.verticalLayout9_Secretaries_1.addWidget(self.dateEditVacatedDate_Secretary_1)

        # Secretaries 2 ----------------------------------------------------------------------
        self.labelSecretaries_2_Name = QLabel('Secretaries 2:')
        self.lineEditSecretariesName_2 = QLineEdit()
        self.lineEditSecretariesName_2.setText(self.selectedRow1[30])

        self.labelAppointedDate_Secretary_2 = QLabel('Appointed Date')
        self.labelResignedDate_Secretary_2 = QLabel('Resigned Date')
        self.labelVacatedDate_Secretary_2 = QLabel('Vacated Date')

        self.newDateEditAppointedDate_Secretary_2 = self.selectedRow1[31]
        self.setDateNewDateEditAppointedDate_Secretary_2String = QDate.fromString(
            self.newDateEditAppointedDate_Secretary_2, "d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_2 = QDateEdit()  # <-------------------------------------------------------- Sec 2 -29,30,21
        self.dateEditAppointedDate_Secretary_2.setDisplayFormat("d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_2.setDate(self.setDateNewDateEditAppointedDate_Secretary_2String)

        self.newDateEditResignedDate_Secretary_2 = self.selectedRow1[32]
        self.setDateNewDateEditResignedDate_Secretary_2String = QDate.fromString(
            self.newDateEditResignedDate_Secretary_2, "d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_2 = QDateEdit()
        self.dateEditResignedDate_Secretary_2.setDisplayFormat("d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_2.setDate(self.setDateNewDateEditResignedDate_Secretary_2String)

        self.newDateEditVacatedDate_Secretary_2 = self.selectedRow1[33]
        self.setDateNewDateEditVacatedDate_Secretary_2String = QDate.fromString(self.newDateEditVacatedDate_Secretary_2,
                                                                                "d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_2 = QDateEdit()
        self.dateEditVacatedDate_Secretary_2.setDisplayFormat("d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_2.setDate(self.setDateNewDateEditVacatedDate_Secretary_2String)

        # Vertical Layouts 10

        self.verticalLayout10_Secretaries_2 = QVBoxLayout()
        self.verticalLayout10_Secretaries_2.addWidget(self.labelSecretaries_2_Name)
        self.verticalLayout10_Secretaries_2.addWidget(self.lineEditSecretariesName_2)

        self.verticalLayout10_Secretaries_2.addWidget(self.labelAppointedDate_Secretary_2)
        self.verticalLayout10_Secretaries_2.addWidget(self.dateEditAppointedDate_Secretary_2)
        self.verticalLayout10_Secretaries_2.addWidget(self.labelResignedDate_Secretary_2)
        self.verticalLayout10_Secretaries_2.addWidget(self.dateEditResignedDate_Secretary_2)
        self.verticalLayout10_Secretaries_2.addWidget(self.labelVacatedDate_Secretary_2)
        self.verticalLayout10_Secretaries_2.addWidget(self.dateEditVacatedDate_Secretary_2)

        # Vertical Layout 10

        # Secretaries Horizontal Layout add vertical layout 9 & 10 here

        self.horizontalLayout_6_Secretaries = QHBoxLayout()
        self.horizontalLayout_6_Secretaries.addLayout(self.verticalLayout9_Secretaries_1)
        self.horizontalLayout_6_Secretaries.addLayout(self.verticalLayout10_Secretaries_2)

        # Final Horizontal Line
        self.labelPreparedBy = QLabel('Prepared By')
        self.labelScannedBy = QLabel('Scanned By')
        self.labelCheckedBy = QLabel('Checked By')

        self.verticalLayout11_Prepared = QVBoxLayout()
        self.verticalLayout11_Prepared.addWidget(self.labelPreparedBy)
        self.verticalLayout11_Prepared.addWidget(self.labelScannedBy)
        self.verticalLayout11_Prepared.addWidget(self.labelCheckedBy)

        self.lineEditPreparedBy = QLineEdit()
        self.lineEditPreparedBy.setText(self.selectedRow1[37])
        self.lineEditCheckedBy = QLineEdit()
        self.lineEditCheckedBy.setText(self.selectedRow1[41])
        self.lineEditScannedBy = QLineEdit()
        self.lineEditScannedBy.setText(self.selectedRow1[39])

        self.verticalLayout12_linePrepared = QVBoxLayout()
        self.verticalLayout12_linePrepared.addWidget(self.lineEditPreparedBy)
        self.verticalLayout12_linePrepared.addWidget(self.lineEditCheckedBy)
        self.verticalLayout12_linePrepared.addWidget(self.lineEditScannedBy)

        self.newDateEditPrepared = self.selectedRow1[38]
        self.setDateNewDateEditPreparedString = QDate.fromString(self.newDateEditPrepared, "d-MMM-yyyy")
        self.dateEditPrepared = QDateEdit()  # <-------------------------------------------------------- Date Prep36
        self.dateEditPrepared.setDisplayFormat("d-MMM-yyyy")
        self.dateEditPrepared.setDate(self.setDateNewDateEditPreparedString)

        self.newDateEditScanned = self.selectedRow1[40]
        self.setDateNewDateEditScannedString = QDate.fromString(self.newDateEditScanned, "d-MMM-yyyy")
        self.dateEditScanned = QDateEdit()  # <-------------------------------------------------------- Date Scanned40
        self.dateEditScanned.setDisplayFormat("d-MMM-yyyy")
        self.dateEditScanned.setDate(self.setDateNewDateEditScannedString)

        self.newDateEditChecked = self.selectedRow1[42]
        self.setDateNewDateEditCheckedString = QDate.fromString(self.newDateEditChecked, "d-MMM-yyyy")
        self.dateEditChecked = QDateEdit()  # <-------------------------------------------------------- Date Checked38
        self.dateEditChecked.setDisplayFormat("d-MMM-yyyy")
        self.dateEditChecked.setDate(self.setDateNewDateEditCheckedString)

        self.verticalLayout13_datePrepared = QVBoxLayout()
        self.verticalLayout13_datePrepared.addWidget(self.dateEditPrepared)
        self.verticalLayout13_datePrepared.addWidget(self.dateEditScanned)
        self.verticalLayout13_datePrepared.addWidget(self.dateEditChecked)

        self.horizontalLayout_7_PreparedScannedChecked = QHBoxLayout()
        self.horizontalLayout_7_PreparedScannedChecked.addLayout(self.verticalLayout11_Prepared)
        self.horizontalLayout_7_PreparedScannedChecked.addLayout(self.verticalLayout12_linePrepared)
        self.horizontalLayout_7_PreparedScannedChecked.addLayout(self.verticalLayout13_datePrepared)

        self.mainLayoutTab1 = QVBoxLayout()  # The final main layout

        self.mainLayoutTab1.addLayout(self.comboHBoxLayout)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_1)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_2)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_3_RegBusiness_Add)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_4_NatureOfBusiness)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_5_DirectorAndContact)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_6_Secretaries)
        self.mainLayoutTab1.addLayout(self.horizontalLayout_7_PreparedScannedChecked)

        # Buttons cased in an Horizontal Layout
        self.buttonHorizontal = QHBoxLayout()
        self.buttonPreviousRecord = QPushButton('Previous Record')
        self.buttonHorizontal.addWidget(self.buttonPreviousRecord)
        self.buttonNextRecord = QPushButton('Next Record')
        self.buttonHorizontal.addWidget(self.buttonNextRecord)
        self.buttonUpdateRecord = QPushButton('Update Record')
        self.buttonHorizontal.addWidget(self.buttonUpdateRecord)
        self.buttonCancelCloseWindow = QPushButton('Cancel')
        self.buttonHorizontal.addWidget(self.buttonCancelCloseWindow)

        self.mainLayoutTab1.addSpacing(50)
        self.mainLayoutTab1.addLayout(self.buttonHorizontal)

        # Scroll Area ________________________________________________________________________________________________
        self.scrollingWidget = QWidget()
        self.scrollingWidget.setLayout(self.mainLayoutTab1)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollingWidget)

        self.parentMainLayout = QVBoxLayout(self)
        self.parentMainLayout.addWidget(self.scrollArea)
        # ____________________________________________________________________________________________________________________

        # self.setLayout(self.mainLayoutTab1)

        # Submit Record Button Functionality
        self.buttonPreviousRecord.clicked.connect(self.previousRecord)
        self.buttonNextRecord.clicked.connect(self.nextRecord)
        self.buttonUpdateRecord.clicked.connect(self.updateRecord)
        self.buttonCancelCloseWindow.clicked.connect(self.closeWindowMessage)

    def setComboBoxToFirstCoName(self):
        self.companyNameWhenDeepViewOpens = self.selectedRow1[1]  # this retrieves the company name when the deep view first opens, this will be used in the following
        # set the combo box as well, so they are uniform and would not have any issues when updating new record to db
        self.comboBoxDeepView.setCurrentText(self.selectedRow1[1])  # sets the combobox to the company it opens with or company that was selected in the output table

    def previousRecord(self):
        """ Here we are able to move forward up to the end of the list of companies (as listed in the combobox), we can also move backwards till the first company, and not
        before that, the self.currentIndex will stop once it equates to '0' """

        self.currentIndex = self.comboBoxDeepView.currentIndex()

        if self.currentIndex == 0:
            customMessage("There are no earlier records")
        else:
            self.currentIndex = self.comboBoxDeepView.currentIndex()
            self.prevCompanyButton = (self.comboBoxList[self.currentIndex - 1])  # this will give us the next company from the combobox to be selected when the "Next" button is clicked

            try:
                self.conn = sqlite3.connect(self.databaseName)
                self.c = self.conn.cursor()

                self.query = (f""" SELECT * FROM {self.tableName} WHERE CoName = '{self.prevCompanyButton}' """)
                self.c.execute(self.query)
                self.comboBoxSelectionData = self.c.execute(self.query)
                self.comboBoxSelectionData = self.comboBoxSelectionData.fetchone()
                self.comboBoxSelectionDataFieldInput()
            except:
                print('Unable to pull data from DB')

            self.comboBoxDeepView.setCurrentIndex(self.currentIndex - 1)

    def nextRecord(self):
        """ Here we are able to move forward up to the end of the list of companies (as listed in the combobox), so remember this is unlike the
        stackedwidget next and previous buttons where you can make a circular movement meaning start to end and back to start. Here we move
        from start to end and stops there, we would need to get back to start the same way we came back manually using the either the previous button
        or the comboboz pull down menu"""

        try:
            self.currentIndex = self.comboBoxDeepView.currentIndex()
            self.nextCompanyButton = (self.comboBoxList[
                self.currentIndex + 1])  # this will give us the next company from the combobox to be selected when the "Next" button is clicked

            try:
                self.conn = sqlite3.connect(self.databaseName)
                self.c = self.conn.cursor()

                # self.query = f"SELECT * FROM {self.tableName} WHERE CoName = {self.CoName}"
                self.query = (f""" SELECT * FROM {self.tableName} WHERE CoName = '{self.nextCompanyButton}' """)
                self.c.execute(self.query)
                self.comboBoxSelectionData = self.c.execute(self.query)
                self.comboBoxSelectionData = self.comboBoxSelectionData.fetchone()
                self.comboBoxSelectionDataFieldInput()
            except:
                print('Unable to pull data from DB')

            self.comboBoxDeepView.setCurrentIndex(self.currentIndex + 1)

        except:
            customMessage("Unable to retrieve next record")

    def updateRecord(self):
        # This selects the current Company Name from the Combo Box, we can use this to update the relevant table
        self.comboBoxSelection = self.comboBoxDeepView.currentText()

        self.FileNo = self.lineEdit_3_FileNo.text()
        self.CoName = self.lineEdit_coName.text()
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
        # ------------------------------------------------------------------------------------------------------------
        self.Secretaries1 = self.lineEditSecretariesName_1.text()
        self.Secretaries1AppointedDate = self.dateEditAppointedDate_Secretary_1.text()
        self.Secretaries1ResignedDate = self.dateEditResignedDate_Secretary_1.text()
        self.Secretaries1VacatedDate = self.dateEditVacatedDate_Secretary_1.text()

        self.Secretaries2 = self.lineEditSecretariesName_2.text()
        self.Secretaries2AppointedDate = self.dateEditAppointedDate_Secretary_2.text()
        self.Secretaries2ResignedDate = self.dateEditResignedDate_Secretary_2.text()
        self.Secretaries2VacatedDate = self.dateEditVacatedDate_Secretary_2.text()

        # ------------------------------------------------------------------------------------------------------------
        self.ContactPerson = self.lineEditContactPerson.text()
        self.ContactPersonTel = self.lineEditContactTel.text()
        self.ContactPersonEmail = self.lineEditContactEmail.text()

        self.PreparedBy = self.lineEditPreparedBy.text()
        self.PreparedDate = self.dateEditPrepared.text()
        self.ScannedBy = self.lineEditScannedBy.text()
        self.ScannedDate = self.dateEditScanned.text()
        self.CheckedBy = self.lineEditCheckedBy.text()
        self.CheckedDate = self.dateEditChecked.text()

        self.whenComboBoxIsChanged()

        # print(self.comboBoxSelectionData)

        # print(f"From DB  36: {self.comboBoxSelectionData[36]}")
        # print(f"From Display  36: {self.PreparedDate}")
        # print(f"From DB  38: {self.comboBoxSelectionData[38]}")
        # print(f"From Display 38 : {self.ScannedDate}")
        # print(f"From DB 40: {self.comboBoxSelectionData[40]}")
        # print(f"From Display 40 : {self.CheckedDate}")

        try:
            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()

            test = "test"
            self.query = (f""" UPDATE {self.tableName} SET
                                     FileNo = '{self.FileNo}', 
                                     CoName = '{self.CoName}',
                                     CoOldName = '{self.CoOldName}',
                                     RegNO = '{self.RegNO}',
                                     DateOfChange = '{self.DateOfChange}',
                                     IncDate = '{self.IncDate}',

                                     RegisteredAdd = '{self.RegisteredAdd}',
                                     BusinessAdd = '{self.BusinessAdd}',
                                     NatureOfBusiness = '{self.NatureOfBusiness}',
                                     PaidUpCapital = '{self.PaidUpCapital}',
                                     Member1 = '{self.Member1}',
                                     Member1_Shares = '{self.Member1_Shares}',
                                     Member2 = '{self.Member2}',
                                     Member2_Shares = '{self.Member2_Shares}',
                                     Member3 = '{self.Member3}',
                                     Member3_Shares = '{self.Member3_Shares}',
                                     Member4 = '{self.Member4}',
                                     Member4_Shares = '{self.Member4_Shares}',
                                     Member5 = '{self.Member5}',
                                     Member5_Shares = '{self.Member5_Shares}',
                                     
                                     Director1 = '{self.Director1}',
                                     Director2 = '{self.Director2}',
                                     Director3 = '{self.Director3}',
                                     Director4 = '{self.Director4}',
                                     Director5 = '{self.Director5}',

                                     Secretaries1 = '{self.Secretaries1}',
                                     Sec1_Appointed_Date = '{self.Secretaries1AppointedDate}',
                                     Sec1_Resigned_Date = '{self.Secretaries1ResignedDate}',
                                     Sec1_Vacated_Date = '{self.Secretaries1VacatedDate}',
                                     
                                     Secretaries2 = '{self.Secretaries2}',
                                     Sec2_Appointed_Date = '{self.Secretaries2AppointedDate}',
                                     Sec2_Resigned_Date = '{self.Secretaries2ResignedDate}',
                                     Sec2_Vacated_Date = '{self.Secretaries2VacatedDate}',

                                     ContactPerson = '{self.ContactPerson}',
                                     ContactPersonTel = '{self.ContactPersonTel}',
                                     ContactPersonEmail = '{self.ContactPersonEmail}',
                                     PreparedBy = '{self.PreparedBy}',
                                     PreparedDate = '{self.PreparedDate}',
                                     ScannedBy = '{self.ScannedBy}',
                                     ScannedDate = '{self.ScannedDate}',
                                     CheckedBy = '{self.CheckedBy}',
                                     CheckedDate = '{self.CheckedDate}'


                               WHERE CoName = '{self.comboBoxSelection}' """)

            self.c.execute(self.query)
            self.conn.commit()
        except:
            customMessage(f"Unable to update with new records, please check update function")

    def comboBoxCompanyList(self):

        """ this connects to the db and pulls the records from the CoName field
        which is used to populate the ComboBox list. You will see a for loop below
        that is used to populate the db query into a list which is then used by the ComboBox."""

        ######################################################
        # new db
        ######################################################

        # Database connect and query table for combobox company list
        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()
        self.query = f"SELECT CoName FROM {self.tableName}"
        self.c.execute(self.query)
        self.searchComboBox = self.c.execute(
            self.query)  # This is purely Python, not PyQt, the ComboBox is only set up at below using the same name

        self.comboBoxList = []  # Python List that used to add items to the searchComboBox (This is Python not PyQt)
        for company in self.searchComboBox:
            self.comboBoxList.append(company[0])

    def ifComboBoxItemSelected(self):
        self.comboBoxDeepView.currentIndexChanged.connect(self.whenComboBoxIsChanged)

    def whenComboBoxIsChanged(self):

        self.comboBoxSelection = self.comboBoxDeepView.currentText()
        # print(self.comboBoxSelection)

        try:
            self.conn = sqlite3.connect(self.databaseName)
            self.c = self.conn.cursor()

            # self.query = f"SELECT * FROM {self.tableName} WHERE CoName = {self.CoName}"
            self.query = (f""" SELECT * FROM {self.tableName} WHERE CoName = '{self.comboBoxSelection}' """)
            self.c.execute(self.query)
            self.comboBoxSelectionData = self.c.execute(self.query)
            self.comboBoxSelectionData = self.comboBoxSelectionData.fetchone()
            self.comboBoxSelectionDataFieldInput()


        except:

            print('Unable to pull data from DB')

    def comboBoxSelectionDataFieldInput(self):

        # print(self.comboBoxSelectionData) --> prints all the data points from the database according to the ComboBox Selection
        self.lineEdit_3_FileNo.setText(self.comboBoxSelectionData[0])
        self.lineEdit_coName.setText(self.comboBoxSelectionData[1])  # <-------------------------------------------
        self.lineEdit_coOldName.setText(self.comboBoxSelectionData[2])  # <-------------------------------------------
        self.lineEdit_regNo.setText(self.comboBoxSelectionData[3])  # <-------------------------------------------

        # Horizontal Line 2 : Date Change

        self.newDateEditDateOfChange = self.comboBoxSelectionData[4]  # <-------------------------------------------
        self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")
        #
        # self.dateEditDateOfChange = QDateEdit()
        # self.dateEditDateOfChange.setDisplayFormat("d-MMM-yyyy")
        self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)

        # self.newDateEditDateOfChange = self.comboBoxSelectionData[4] #<-------------------------------------------
        # self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")
        # self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)

        # Horizontal Line 2 : Date Incorporated
        self.newDateEditIncorporatedDate = self.comboBoxSelectionData[5]  # <-------------------------------------------
        self.setDateNewDateEditIncorporatedDateString = QDate.fromString(self.newDateEditIncorporatedDate, "d-MMM-yyyy")
        # self.dateEditIncorporatedDate = QDateEdit()
        # self.dateEditIncorporatedDate.setDisplayFormat("d-MMM-yyyy")
        self.dateEditIncorporatedDate.setDate(self.setDateNewDateEditIncorporatedDateString)

        # Vertical Layout: Type of Company
        self.radioButtonTypeVerticalLayout_1 = QVBoxLayout()
        self.typeLabel = QLabel('Type')
        self.typeLabelBlank = QLabel('')  # This is used to insert blank spacing

        # Radio Buttons: Type of Company

        # if self.comboBoxSelectionData[6] == 'Limited By Shares':
        #     self.typeRadioButton_1.setChecked(True)
        # elif self.comboBoxSelectionData[6] == 'Private Limited':
        #     self.typeRadioButton_2.setChecked(True)
        # else:
        #     pass

        # Radio Button Group: Type of Company
        # self.radioButtonGroup_Company_Type = QButtonGroup(self)
        # self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_1)
        # self.radioButtonGroup_Company_Type.addButton(self.typeRadioButton_2)
        # # self.radioButtonGroup_Company_Type.checkedButton() #<------------------------------------- Radio Button Type
        #
        #
        # # Radio Buttons: Status of Company

        # if self.comboBoxSelectionData[6] == 'Existing':
        #     self.statusRadioButton_1.setChecked(True)
        # elif self.comboBoxSelectionData[6] == 'Dissolved':
        #     self.statusRadioButton_2.setChecked(True)
        # elif self.comboBoxSelectionData[6] == 'Winding Up':
        #     self.statusRadioButton_3.setChecked(True)
        # else:
        #     pass
        #
        # # Radio Button Group: Status of Company
        # self.radioButtonGroup_Company_Status = QButtonGroup(self)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_1)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_2)
        # self.radioButtonGroup_Company_Status.addButton(self.statusRadioButton_3)

        # Horizontal Layout 3: Registered & Business Address ######################################################################################

        # Registered & Business Address

        self.lineRegisteredAdd.setText(self.comboBoxSelectionData[7])  # <-------------------------------------------
        self.lineBusinessAdd.setText(self.comboBoxSelectionData[8])  # <-------------------------------------------
        self.lineEditNatureOfBusiness.setText(
            self.comboBoxSelectionData[9])  # <-------------------------------------------

        self.lineEditPaidUpCapital.setText(
            self.comboBoxSelectionData[10])  # <-------------------------------------------

        self.editMembers_1.setText(self.comboBoxSelectionData[11])  # <-------------------------------------------
        self.editMembers_2.setText(self.comboBoxSelectionData[13])  # <-------------------------------------------
        self.editMembers_3.setText(self.comboBoxSelectionData[15])  # <-------------------------------------------
        self.editMembers_4.setText(self.comboBoxSelectionData[17])  # <-------------------------------------------
        self.editMembers_5.setText(self.comboBoxSelectionData[19])  # <-------------------------------------------

        self.lineEditShares_1.setText(self.comboBoxSelectionData[12])
        self.lineEditShares_2.setText(self.comboBoxSelectionData[14])
        self.lineEditShares_3.setText(self.comboBoxSelectionData[16])
        self.lineEditShares_4.setText(self.comboBoxSelectionData[18])
        self.lineEditShares_5.setText(self.comboBoxSelectionData[20])

        self.lineEditDirectorName_1.setText(self.comboBoxSelectionData[21])
        self.lineEditDirectorName_2.setText(self.comboBoxSelectionData[22])
        self.lineEditDirectorName_3.setText(self.comboBoxSelectionData[23])
        self.lineEditDirectorName_4.setText(self.comboBoxSelectionData[24])
        self.lineEditDirectorName_5.setText(self.comboBoxSelectionData[25])

        self.lineEditContactPerson.setText(self.comboBoxSelectionData[34])
        self.lineEditContactTel.setText(self.comboBoxSelectionData[35])
        self.lineEditContactEmail.setText(self.comboBoxSelectionData[36])

        # Secretaries 1 ----------------------------------------------------------------------
        self.lineEditSecretariesName_1.setText(self.comboBoxSelectionData[26])

        # self.newDateEditDateOfChange = self.comboBoxSelectionData[4] #<-------------------------------------------
        # self.setDateNewDateEditDateOfChangeString = QDate.fromString(self.newDateEditDateOfChange, "d-MMM-yyyy")
        # self.dateEditDateOfChange.setDate(self.setDateNewDateEditDateOfChangeString)

        self.newDateEditAppointedDate_Secretary_1 = self.comboBoxSelectionData[
            27]  # <-------------------------------------------
        self.setDateNewDateEditAppointedDate_Secretary_1String = QDate.fromString(
            self.newDateEditAppointedDate_Secretary_1, "d-MMM-yyyy")
        # self.dateEditAppointedDate_Secretary_1 = QDateEdit()
        # self.dateEditAppointedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_1.setDate(self.setDateNewDateEditAppointedDate_Secretary_1String)

        self.newDateEditResignedDate_Secretary_1 = self.comboBoxSelectionData[
            28]  # <-------------------------------------------
        self.setDateNewDateEditResignedDate_Secretary_1String = QDate.fromString(
            self.newDateEditResignedDate_Secretary_1, "d-MMM-yyyy")
        # self.dateEditResignedDate_Secretary_1 = QDateEdit()
        # self.dateEditResignedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_1.setDate(self.setDateNewDateEditResignedDate_Secretary_1String)

        self.newDateEditVacatedDate_Secretary_1 = self.comboBoxSelectionData[
            29]  # <-------------------------------------------
        self.setDateNewDateEditVacatedDate_Secretary_1String = QDate.fromString(self.newDateEditVacatedDate_Secretary_1,
                                                                                "d-MMM-yyyy")
        # self.dateEditVacatedDate_Secretary_1 = QDateEdit()
        # self.dateEditVacatedDate_Secretary_1.setDisplayFormat("d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_1.setDate(self.setDateNewDateEditVacatedDate_Secretary_1String)

        # Secretaries 2 ----------------------------------------------------------------------

        self.lineEditSecretariesName_2.setText(self.comboBoxSelectionData[30])

        self.newDateEditAppointedDate_Secretary_2 = self.comboBoxSelectionData[
            31]  # <-------------------------------------------
        self.setDateNewDateEditAppointedDate_Secretary_2String = QDate.fromString(
            self.newDateEditAppointedDate_Secretary_2, "d-MMM-yyyy")
        self.dateEditAppointedDate_Secretary_2.setDate(self.setDateNewDateEditAppointedDate_Secretary_2String)

        self.newDateEditResignedDate_Secretary_2 = self.comboBoxSelectionData[
            32]  # <-------------------------------------------
        self.setDateNewDateEditResignedDate_Secretary_2String = QDate.fromString(
            self.newDateEditResignedDate_Secretary_2, "d-MMM-yyyy")
        self.dateEditResignedDate_Secretary_2.setDate(self.setDateNewDateEditResignedDate_Secretary_2String)

        self.newDateEditVacatedDate_Secretary_2 = self.comboBoxSelectionData[
            33]  # <-------------------------------------------
        self.setDateNewDateEditVacatedDate_Secretary_2String = QDate.fromString(self.newDateEditVacatedDate_Secretary_2,
                                                                                "d-MMM-yyyy")
        self.dateEditVacatedDate_Secretary_2.setDate(self.setDateNewDateEditVacatedDate_Secretary_2String)

        self.lineEditPreparedBy.setText(self.comboBoxSelectionData[37])
        self.lineEditCheckedBy.setText(self.comboBoxSelectionData[39])
        self.lineEditScannedBy.setText(self.comboBoxSelectionData[41])

        self.newDateEditPrepared = self.comboBoxSelectionData[38]  # <-------------------------------------------
        self.setDateNewDateEditPreparedString = QDate.fromString(self.newDateEditPrepared, "d-MMM-yyyy")
        self.dateEditPrepared.setDate(self.setDateNewDateEditPreparedString)

        self.newDateEditScanned = self.comboBoxSelectionData[40]  # <-------------------------------------------
        self.setDateNewDateEditScannedString = QDate.fromString(self.newDateEditScanned, "d-MMM-yyyy")
        self.dateEditScanned.setDate(self.setDateNewDateEditScannedString)

        self.newDateEditChecked = self.comboBoxSelectionData[42]  # <-------------------------------------------
        self.setDateNewDateEditCheckedString = QDate.fromString(self.newDateEditChecked, "d-MMM-yyyy")
        self.dateEditChecked.setDate(self.setDateNewDateEditCheckedString)

    def closeUpdateWindow(self):

        try:
            updateWindow = self.window()
            updateWindow.close()
        except:
            customMessage('Cannot cancel, close and try again')

    def closeWindowMessage(self):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Close without updating records?")
        msgBox.setWindowTitle("Close Update Window")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.closeUpdateWindow()
        else:
            pass



