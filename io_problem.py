""" 
io_problem.py
Antonio Magaña Reynoso - 218744856
Seminario de Solucion de Problemas de Sistemas Operativos - D05
"""

import sys
from time import sleep

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QRunnable,
                            Qt, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
                               QLineEdit, QMainWindow, QProgressBar,
                               QPushButton, QWidget)


class SignalProcess(QObject):
    wait_input = Signal()
    resume = Signal()
    finished = Signal()


class RunProcess(QRunnable):
    def __init__(self, signal: SignalProcess, status: QLabel, progress: QProgressBar) -> None:
        super().__init__()
        self.signal = signal
        self.status = status
        self.progress = progress

    @Slot()
    def run(self) -> None:
        self.status.setText('En ejecución')
        for s in range(6):
            self.progress.setValue(self.progress.value() + 10)
            sleep(1.0)

        self.status.setText('En espera de entrada')
        self.signal.wait_input.emit()

    def resume(self):
        self.status.setText('En ejecución')
        for s in range(4):
            self.progress.setValue(self.progress.value() + 10)
            sleep(1.0)

        self.status.setText('Terminado')
        self.signal.finished.emit()


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

        # Vars
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(4)

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
        self.pushButton_continue1.clicked.connect(self.resume_p1)

        self.pushButton_continue2 = QPushButton(self.centralwidget)
        self.pushButton_continue2.setObjectName(u"pushButton_continue2")
        self.pushButton_continue2.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton_continue2, 4, 6, 1, 1)
        self.pushButton_continue2.clicked.connect(self.resume_p2)

        self.pushButton_start_execution = QPushButton(self.centralwidget)
        self.pushButton_start_execution.setObjectName(
            u"pushButton_start_execution")
        self.gridLayout.addWidget(self.pushButton_start_execution, 8, 3, 1, 2)
        self.pushButton_start_execution.clicked.connect(self.start_execution)

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

    def start_execution(self):
        print('starting!')
        self.signal_p1 = SignalProcess()
        self.p1 = RunProcess(
            self.signal_p1, self.label_status_p1, self.progressBar_p1)
        self.p1.signal.wait_input.connect(self.waiting_input_p1)
        self.p1.signal.resume.connect(self.p1.resume)
        self.p1.signal.finished.connect(self.finish_p1)

        self.signal_p2 = SignalProcess()
        self.p2 = RunProcess(
            self.signal_p2, self.label_status_p2, self.progressBar_p2)
        self.p2.signal.wait_input.connect(self.waiting_input_p2)
        self.p2.signal.resume.connect(self.p2.resume)
        self.p2.signal.finished.connect(self.finish_p2)

        self.signal_p3 = SignalProcess()
        self.p3 = RunProcess(
            self.signal_p3, self.label_status_p3, self.progressBar_p3)
        self.p3.signal.wait_input.connect(self.waiting_input_p3)
        self.p3.signal.resume.connect(self.p3.resume)
        self.p3.signal.finished.connect(self.finish_p3)

        self.thread_pool.start(self.p1)
    # start_execution

    def waiting_input_p1(self):
        self.lineEdit_p1.setEnabled(True)
        self.pushButton_continue1.setEnabled(True)
    # waiting_input_p1

    def waiting_input_p2(self):
        self.lineEdit_p2.setEnabled(True)
        self.pushButton_continue2.setEnabled(True)
    # waiting_input_p2

    def waiting_input_p3(self):
        self.p3.signal.resume.emit()
    # waiting_input_p3

    def resume_p1(self):
        self.p1_result = self.lineEdit_p1.text()
        if self.p1_result:
            print(self.p1_result)
            self.lineEdit_p1.setEnabled(False)
            self.pushButton_continue1.setEnabled(False)

            self.p1.signal.resume.emit()
        else:
            print('nothing!')
    # resume_p1

    def resume_p2(self):
        self.p2_result = self.lineEdit_p2.text()
        if self.p2_result:
            print(self.p2_result)
            self.lineEdit_p2.setEnabled(False)
            self.pushButton_continue2.setEnabled(False)

            self.p2.signal.resume.emit()
        else:
            print('nothing!')
    # resume_p2

    def finish_p1(self):
        print('starting p2')
        self.thread_pool.start(self.p2)
    # finish_p1

    def finish_p2(self):
        print('starting p3')
        self.thread_pool.start(self.p3)
    # finish_p2

    def finish_p3(self):
        self.lineEdit_p3.setText(f'{self.p1_result} {self.p2_result}')
        print('finished p3')
    # finish_p3


if __name__ == '__main__':
    app = QApplication([])
    window = IOProblemWindow()
    window.show()
    sys.exit(app.exec())
