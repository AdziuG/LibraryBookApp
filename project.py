from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# import ui

from delete_dialog import Ui_delete_dialog as Ui_Delete_Dialog
from edit_dialog import Ui_Dialog as Ui_Edit_Dialog
from main_window import Ui_MainWindow
from add_book_dialog import Ui_Dialog as Ui_Add_Dialog
import store_functions as lib

# ADD DIALOG
class AddDialog(QDialog):
    def __init__(self):
        super(AddDialog, self).__init__()
        self.ui = Ui_Add_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

# MAIN WINDOW
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.new_book_btn.pressed.connect(self.show_add_dialog)

    def save_new_book(self, ui):
        # dictionary to store information
        new_book = {
            'id': int(ui.id_spinbox.text()),
            'name': ui.name_input.text(),
            'description': ui.description_input.text(),
            'isbn': ui.description_input_2.text(),
            'page_count': ui.page_count_spinbox.text(),
            'issued': ui.yes.isChecked(),
            'author': ui.author_input.text(),
            'year': int(ui.page_count_spinbox_2.text())
        }
        # check is all cells are fill in
        for attr in new_book:
            if new_book[attr] is None or str(new_book[attr]) == "":
                return False
        lib.add_books(new_book)

    def show_add_dialog(self):
        input_dlg = AddDialog()
        input_dlg.ui.buttonBox.accepted.connect(lambda: self.save_new_book(input_dlg.ui))
        input_dlg.exec()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
