from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# import ui
from delete_dialog import Ui_delete_dialog as Ui_Delete_Dialog
from edit_dialog import Ui_Dialog as Ui_Edit_Dialog
from main_window import Ui_MainWindow
from add_book_dialog import Ui_Dialog as Ui_Add_Dialog
import store_functions as lib


# DELETE WINDOW
class Delete_Dialog(QDialog):
    """
    In this window display information about delete specific item.
    """
    def __init__(self, parent=None):
        super(Delete_Dialog, self).__init__(parent)
        self.ui = Ui_Delete_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)


# EDIT WINDOW
class EditDialog(QDialog):
    """
    Additional window displays when user clicked edit button.
    It's window where user could change specific item.
    """
    def __init__(self):
        super(EditDialog, self).__init__()
        self.ui = Ui_Edit_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)


# ADD WINDOW
class AddDialog(QDialog):
    """
    Additional window displays when user clicked add button.
    It's window where user could add new book.
    """
    def __init__(self):
        super(AddDialog, self).__init__()
        self.ui = Ui_Add_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)


# MAIN WINDOW OF APPLICATION
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.new_book_btn.pressed.connect(self.show_add_dialog)  # pressed button emits signal to func shows window with form to add new book
        self.load_issued_table()
        self.load_unissued_table()
        self.load_all_books_table()

        # Clicked buttons responsible for managing issued book table
        self.edit_issued.clicked.connect(lambda: self.edit_book(self.issued_books_table))
        self.delete_issued.clicked.connect(lambda: self.delete_book(self.issued_books_table))
        self.refresh_issued.clicked.connect(self.load_issued_table)

        # Clicked buttons responsible for manage unissued book table
        self.edit_unissued.clicked.connect(lambda: self.edit_book(self.unissued_books_table))
        self.delete_unissued.clicked.connect(lambda: self.delete_book(self.unissued_books_table))
        self.refresh_unissued.clicked.connect(self.load_unissued_table)

        self.refresh_btn.clicked.connect(self.load_all_books_table)  # btn responsible for refreshing view in the table
        self.search_btn.clicked.connect(self.search_book)

    def save_existing_book(self, ui):
        """
        Method create dictionary type. Gather information from form in GUI and pass it to update book method
        """
        book = {
            'id': int(ui.id_spinbox.text()),
            'name': ui.name_input.text(),
            'description': ui.description_input.text(),
            'isbn': ui.description_input_2.text(),
            'page_count': ui.page_count_spinbox.text(),
            'issued': ui.yes.isChecked(),
            'author': ui.author_input.text(),
            'year': int(ui.page_count_spinbox_2.text())
        }
        lib.update_book(book)

    def edit_book(self, table):
        """
        Method get information from table (using current selected row search specific id).
        After that load information to form in GUI. After that call slot and passes changed data to save existing func.
        :param table could be issued table or unissued table
        """
        selected_row = table.currentRow()
        # if nothing is selected then selected row = -1
        if selected_row != -1:
            book_id = int(table.item(selected_row, 0).text())
            book = lib.find_book(book_id)
            # Creating the dialog
            dialog = EditDialog()
            dialog.ui.id_spinbox.setValue(int(book_id))
            dialog.ui.name_input.setText(book.name)
            dialog.ui.description_input.setText(book.description)
            dialog.ui.description_input_2.setText(book.isbn)
            dialog.ui.page_count_spinbox.setValue(int(book.page_count))
            dialog.ui.yes.setChecked(book.issued)
            if book.issued == False:
                dialog.ui.yes_2.setChecked(True)
            dialog.ui.author_input.setText(book.isbn)
            dialog.ui.page_count_spinbox_2.setValue(int(book.page_count))
            dialog.ui.buttonBox.accepted.connect(lambda: self.save_existing_book(dialog.ui))
            dialog.exec()
            self.load_issued_table()
            self.load_unissued_table()

    def save_new_book(self, ui):
        """
        Create dictionary to store information. Gets data from GUI form.
        Call metgod add books and passes created dict.
        :param ui:
        :return:
        """
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
        self.load_issued_table()    # update issued table
        self.load_unissued_table()  # update unissued table

    def search_book(self):
        """
        Method responsible for searching book. Book is search by id. ID is unique.
        To find specific book using find_book func.
        It's slot func. Signal emits search button.
        :return:
        """
        if self.search_input.text() != "":
            book = lib.find_book(int(self.search_input.text()))
            if book != None:
                self.search_table.setRowCount(1)
                book_dict = book.to_dict()
                # book dict store information about specific book in dictionary
                # loop go through attributes in book and place them to table using setItem.
                for book_index, attr in enumerate(book_dict):
                    self.search_table.setItem(
                        0, book_index, QTableWidgetItem(str(book_dict[str(attr)])))
                    self.search_table.item(0, book_index).setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def delete_book(self, table):
        """
        Method delete selected book. This is slot func. Signal emits delete button.
        :param table:
        :return:
        """
        selected_row = table.currentRow()
        if selected_row != -1:
            book_id = int(table.item(selected_row, 0).text())
            dialog = Delete_Dialog()
            dialog.ui.buttonBox.accepted.connect(lambda: lib.delete_book(book_id))
            dialog.exec()
            self.load_issued_table()
            self.load_unissued_table()

    def load_issued_table(self):
        """
        Loads data to issued table
        :return:
        """
        books = lib.get_issued_books()
        self.issued_books_table.setRowCount((len(books)))  # set rows in this table using length of list of issued book
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.issued_books_table.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.issued_books_table.item(index, book_index).setFlags((Qt.ItemIsSelectable | Qt.ItemIsEnabled))

    def load_unissued_table(self):
        """
        Load data to unissued table
        :return:
        """
        books = lib.get_unissued_books()
        self.unissued_books_table.setRowCount((len(books)))  # set rows in this table using length of list of unissued book
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.unissued_books_table.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.unissued_books_table.item(index, book_index).setFlags((Qt.ItemIsSelectable | Qt.ItemIsEnabled))

    def load_all_books_table(self):
        """
        Method responsible to load data to All Books tab.
        :return:
        """
        books = lib.load_books()
        self.all_books_table.setRowCount((len(books)))  # set rows in this table using length of list all books
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.all_books_table.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.all_books_table.item(index, book_index).setFlags((Qt.ItemIsSelectable | Qt.ItemIsEnabled))

    def show_add_dialog(self):
        input_dlg = AddDialog()
        input_dlg.ui.buttonBox.accepted.connect(lambda: self.save_new_book(input_dlg.ui))
        input_dlg.exec()


app = QApplication([])
# load stylesheet
style_sheet = open("dark_orange/style.qss", 'r')

with style_sheet:
    qss = style_sheet.read()
    app.setStyleSheet(qss)

window = MainWindow()
window.show()
app.exec_()
