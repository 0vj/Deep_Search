# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from res.ui import deep_search_ui
import subprocess
import os


def init(dialog, self):
    self.dir = ''
    self.dir_toolButton.clicked.connect(
        lambda: open_dir(dialog, self)
    )
    self.search_pushButton.clicked.connect(
        lambda: search(dialog, self)
    )
    self.result_tableWidget.doubleClicked.connect(
        lambda: double(dialog, self)
    )


def open_dir(dialog, self):
    self.dir = QtWidgets.QFileDialog.getExistingDirectory(
        dialog, "Select Directory"
        )
    if self.dir != '':
        self.path_lineEdit.setText(self.dir)


def search(dialog, self):
    result = []
    if self.dir != '':
        keywords = self.comma_separated_lineEdit.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda keyword: keyword.strip().lower(), keywords))
        files = os.listdir(self.dir)
        for file_ in files:
            joined = os.path.join(self.dir, file_)
            try:
                if os.path.isfile(joined):
                    with open(joined, 'r') as plain_file:
                        lines = list(map(
                            lambda line: line.lower(),
                            plain_file.readlines()
                            ))
                        for keyword in keywords:
                            c = 0
                            for line in lines:
                                c += 1
                                if keyword in line:
                                    temp = [file_, keyword, str(c)]
                                    result.append(temp)
            except Exception as e:
                print('This is not a text file', str(e))
        row_count = len(result)
        self.result_tableWidget.setRowCount(row_count)
        for row in range(row_count):
            for column in range(3):
                text = result[row][column]
                item = QtWidgets.QTableWidgetItem(text)
                self.result_tableWidget.setItem(row, column, item)


def double(dialog, self):
    open_with = self.open_with_comboBox.currentText()
    current_row = self.result_tableWidget.currentRow()
    if current_row != -1:
        file_ = self.result_tableWidget.item(current_row, 0).text()
        file_ = os.path.join(self.dir, file_)
        subprocess.run('{} "{}"'.format(open_with, file_), shell=True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    ui = deep_search_ui.Ui_dialog()
    ui.setupUi(dialog)
    init(dialog, ui)
    dialog.show()
    sys.exit(app.exec_())
