import sys
import os
import re
from word2pdf import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from win32com.client import gencache
from win32com.client import constants, gencache

count = 0
num_file = 0


class trans(QMainWindow, Ui_MainWindow):  # 继承自父类QtWidgets.QMainWindow
    def __init__(self, parent=None):
        super(trans, self).__init__()  # 因为继承关系，要对父类初始化
        # 通过super初始化父类，__init__()函数无self，若直接QtWidgets.QMainWindow).__init__(self)，括号里是有self的
        self.setupUi(self)
        self.word2pdfButton.clicked.connect(self.word2pdfButton_clicked)
        self.excel2pdfButton.clicked.connect(self.excel2pdfButton_clicked)

    # word转pdf
    def word2pdf(self, wordPath, pdfPath):
        word = gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(wordPath, ReadOnly=1)
        doc.ExportAsFixedFormat(pdfPath,
                                constants.wdExportFormatPDF,
                                Item=constants.wdExportDocumentWithMarkup,
                                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        word.Quit(constants.wdDoNotSaveChanges)

    # excel转pdf
    def excel2pdf(self, excelPath, pdfPath):
        xlApp = gencache.EnsureDispatch('Excel.Application')
        xls = xlApp.Workbooks.Open(excelPath, ReadOnly=1)
        xls.ExportAsFixedFormat(0,  pdfPath)
        xlApp.Quit()

    def word2pdfButton_clicked(self):
        self.word2pdfButton.setEnabled(False)
        self.excel2pdfButton.setEnabled(False)

        self.textBrowser.setPlainText('开始转换')
        QApplication.processEvents()

        for dirs, subdirs, files in os.walk(os.getcwd()):
            for name in files:
                global num_file
                if re.search('\.(doc|docx)', name):
                    num_file += 1
        self.textBrowser.append(("共 %d 个Word文件" % (num_file)))

        for dirs, subdirs, files in os.walk(os.getcwd()):
            for name in files:
                if re.search('\.(doc|docx)', name):
                    global count
                    count = count + 1
                    self.textBrowser.append(
                        ("第 %d / %d 个文件..." % (count, num_file)))
                    self.textBrowser.moveCursor(
                        self.textBrowser.textCursor().End)  # 文本框显示到底部
                    QApplication.processEvents()
                    self.word2pdf(dirs+'\\'+name, dirs+'\\' +
                                  re.subn('(docx|doc)', 'pdf', name)[0])
        self.textBrowser.append('转换完成')
        count = 0
        num_file = 0
        self.word2pdfButton.setEnabled(True)
        self.excel2pdfButton.setEnabled(True)

    def excel2pdfButton_clicked(self):
        self.word2pdfButton.setEnabled(False)
        self.excel2pdfButton.setEnabled(False)
        self.textBrowser.setPlainText('开始转换')
        QApplication.processEvents()
        for dirs, subdirs, files in os.walk(os.getcwd()):
            for name in files:
                global num_file
                if re.search('\.(xlsx|xls)', name):
                    num_file += 1
        self.textBrowser.append(("共 %d 个Excel文件" % (num_file)))

        for dirs, subdirs, files in os.walk(os.getcwd()):
            for name in files:
                if re.search('\.(xlsx|xls)', name):
                    global count
                    count = count + 1
                    self.textBrowser.append(
                        ("第 %d / %d 个文件..." % (count, num_file)))
                    self.textBrowser.moveCursor(
                        self.textBrowser.textCursor().End)  # 文本框显示到底部
                    QApplication.processEvents()

                    self.excel2pdf(dirs+'\\'+name, dirs+'\\' +
                                   re.subn('(xlsx|xls)', 'pdf', name)[0])
        self.textBrowser.append('转换完成')
        count = 0
        num_file = 0
        self.word2pdfButton.setEnabled(True)
        self.excel2pdfButton.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = trans()
    MainWindow.show()
    sys.exit(app.exec_())