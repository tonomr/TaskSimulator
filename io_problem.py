""" 
io_problem.py
Antonio Magaña Reynoso - 218744856
Seminario de Solucion de Problemas de Sistemas Operativos - D05
"""

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
                               QLineEdit, QMainWindow, QProgressBar,
                               QPushButton, QWidget)


class IOProblemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    # __init__

    def setupUi(self, MainWindow):
        """ Create the widgets to setup the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 320)

        # Layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Label
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_title, 0, 2, 1, 3)

        self.label_p1 = QLabel(self.centralwidget)
        self.label_p1.setObjectName(u"label_p1")
        self.label_p1.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_p1, 1, 0, 1, 1)

        self.label_p2 = QLabel(self.centralwidget)
        self.label_p2.setObjectName(u"label_p2")
        self.label_p2.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_p2, 3, 0, 1, 1)

        self.label_p3 = QLabel(self.centralwidget)
        self.label_p3.setObjectName(u"label_p3")
        self.label_p3.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_p3, 5, 1, 1, 1)

        self.label_input1 = QLabel(self.centralwidget)
        self.label_input1.setObjectName(u"label_input1")
        self.label_input1.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_input1, 1, 4, 1, 1)

        self.label_input2 = QLabel(self.centralwidget)
        self.label_input2.setObjectName(u"label_input2")
        self.label_input2.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_input2, 3, 4, 1, 1)

        self.label_output = QLabel(self.centralwidget)
        self.label_output.setObjectName(u"label_output")
        self.label_output.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_output, 5, 5, 1, 1)

        self.label_status_p1 = QLabel(self.centralwidget)
        self.label_status_p1.setObjectName(u"label_status_p1")
        self.label_status_p1.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_status_p1, 1, 1, 1, 1)

        self.label_status_p2 = QLabel(self.centralwidget)
        self.label_status_p2.setObjectName(u"label_status_p2")
        self.label_status_p2.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_status_p2, 3, 1, 1, 1)

        self.label_status_p3 = QLabel(self.centralwidget)
        self.label_status_p3.setObjectName(u"label_status_p3")
        self.label_status_p3.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_status_p3, 5, 2, 1, 1)

        # LineEdit
        self.lineEdit_p1 = QLineEdit(self.centralwidget)
        self.lineEdit_p1.setObjectName(u"lineEdit_p1")
        self.lineEdit_p1.setEnabled(False)
        self.gridLayout.addWidget(self.lineEdit_p1, 2, 4, 1, 2)

        self.lineEdit_p2 = QLineEdit(self.centralwidget)
        self.lineEdit_p2.setObjectName(u"lineEdit_p2")
        self.lineEdit_p2.setEnabled(False)
        self.gridLayout.addWidget(self.lineEdit_p2, 4, 4, 1, 2)

        self.lineEdit_p3 = QLineEdit(self.centralwidget)
        self.lineEdit_p3.setObjectName(u"lineEdit_p3")
        self.lineEdit_p3.setEnabled(True)
        self.lineEdit_p3.setReadOnly(True)
        self.gridLayout.addWidget(self.lineEdit_p3, 6, 5, 1, 2)

        # ProgressBar
        self.progressBar_p1 = QProgressBar(self.centralwidget)
        self.progressBar_p1.setObjectName(u"progressBar_p1")
        self.progressBar_p1.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p1, 2, 0, 1, 3)

        self.progressBar_p2 = QProgressBar(self.centralwidget)
        self.progressBar_p2.setObjectName(u"progressBar_p2")
        self.progressBar_p2.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p2, 4, 0, 1, 3)

        self.progressBar_p3 = QProgressBar(self.centralwidget)
        self.progressBar_p3.setObjectName(u"progressBar_p3")
        self.progressBar_p3.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p3, 6, 0, 1, 4)

        # PushButton
        self.pushButton_continue1 = QPushButton(self.centralwidget)
        self.pushButton_continue1.setObjectName(u"pushButton_continue1")
        self.pushButton_continue1.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton_continue1, 2, 6, 1, 1)

        self.pushButton_continue2 = QPushButton(self.centralwidget)
        self.pushButton_continue2.setObjectName(u"pushButton_continue2")
        self.pushButton_continue2.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton_continue2, 4, 6, 1, 1)

        self.pushButton_start_execution = QPushButton(self.centralwidget)
        self.pushButton_start_execution.setObjectName(
            u"pushButton_start_execution")
        self.gridLayout.addWidget(self.pushButton_start_execution, 8, 3, 1, 2)

        # Line
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 7, 0, 1, 7)

        # Set all widgets in the window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"I/O Problem - AMR", None))
        self.label_p1.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 1", None))
        self.label_p3.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 3", None))
        self.pushButton_continue1.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.pushButton_start_execution.setText(QCoreApplication.translate(
            "MainWindow", u"Empezar Ejecuci\u00f3n", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"Problema de Entrada/Salida", None))
        self.label_input1.setText(QCoreApplication.translate(
            "MainWindow", u"Entrada 1", None))
        self.pushButton_continue2.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.label_input2.setText(QCoreApplication.translate(
            "MainWindow", u"Entrada 2", None))
        self.label_p2.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 2", None))
        self.label_output.setText(
            QCoreApplication.translate("MainWindow", u"Salida", None))
        self.label_status_p1.setText(
            QCoreApplication.translate("MainWindow", u"Inactivo", None))
        self.label_status_p2.setText(
            QCoreApplication.translate("MainWindow", u"Inactivo", None))
        self.label_status_p3.setText(
            QCoreApplication.translate("MainWindow", u"Inactivo", None))
    # retranslateUi


if __name__ == '__main__':
    app = QApplication([])
    window = IOProblemWindow()
    window.show()
    exit(app.exec())
