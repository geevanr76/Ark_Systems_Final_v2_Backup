from PyQt5.QtWidgets import QMessageBox

def customMessage(message):
    submitIncompleteInputToRecordToDBMsg = QMessageBox()
    submitIncompleteInputToRecordToDBMsg.setText(f'{message}')
    submitIncompleteInputToRecordToDBMsg.setIcon(QMessageBox.Information)
    message = submitIncompleteInputToRecordToDBMsg.exec_()

