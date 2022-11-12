""" 
reader-writer_problem.py
Antonio Magaña Reynoso - 218744856
Seminario de Solucion de Problemas de Sistemas Operativos - D05
"""

from sys import exit
from time import sleep

from PySide6.QtCore import (
    QCoreApplication, QMetaObject, Qt, QObject, QRunnable, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout,
                               QLabel, QMainWindow, QPushButton, QWidget)


class SignalProcess(QObject):
    stopped = Signal()


class RunWriter(QRunnable):
    def __init__(self, signal: SignalProcess, status: QLabel):
        super().__init__()
        self.signal = signal
        self.status = status
        self.is_stop = False

    @Slot()
    def run(self) -> None:
        """ Run the writer process for 5seconds or stopped"""
        self.is_stop = False
        self.status.setText('Se esta escribiendo...')

        for s in range(5):
            if self.is_stop:
                break

            sleep(1.0)
            self.status.setText(f'Se esta escribiendo, {4-s}s restantes...')

        self.signal.stopped.emit()
    # run

    def stop(self) -> None:
        """ Stop the writer """
        self.is_stop = True
        self.status.setText('Archivo inactivo')
    # stop
# RunWriter


class RunReader(QRunnable):
    def __init__(self, signal: SignalProcess, status: QLabel):
        super().__init__()
        self.signal = signal
        self.status = status
        self.is_stop = False

    @Slot()
    def run(self):
        """ Run the reader process for 5seconds or stopped """
        self.is_stop = False
        self.status.setText('Se esta leyendo...')

        for s in range(5):
            if self.is_stop:
                break

            sleep(1.0)
            self.status.setText(f'Se esta leyendo, {4-s}s restantes...')

        self.signal.stopped.emit()
    # run

    def stop(self) -> None:
        """ Stop the reader """
        self.is_stop = True
        self.status.setText('Archivo inactivo')
    # stop
# RunReader


class ReaderWriterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow: QMainWindow) -> None:
        """ Create the widgets to setup the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)

        # Layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Vars
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(4)

        # Labels
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Plain)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 3)

        self.label_writer = QLabel(self.centralwidget)
        self.label_writer.setObjectName(u"label_writer")
        self.label_writer.setAlignment(Qt.AlignCenter)
        self.label_writer.setWordWrap(True)
        self.gridLayout.addWidget(self.label_writer, 1, 0, 1, 1)

        self.label_reader = QLabel(self.centralwidget)
        self.label_reader.setObjectName(u"label_reader")
        self.label_reader.setAlignment(Qt.AlignCenter)
        self.label_reader.setWordWrap(True)
        self.gridLayout.addWidget(self.label_reader, 1, 2, 1, 1)

        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_status, 4, 1, 1, 1)

        # Buttons
        self.pushButton_writer = QPushButton(self.centralwidget)
        self.pushButton_writer.setObjectName(u"pushButton_writer")
        self.gridLayout.addWidget(self.pushButton_writer, 2, 0, 1, 1)
        self.pushButton_writer.clicked.connect(self.run_writer)

        self.pushButton_stop_writer = QPushButton(self.centralwidget)
        self.pushButton_stop_writer.setObjectName(
            u"pushButton_stop_writer")
        self.gridLayout.addWidget(self.pushButton_stop_writer, 3, 0, 1, 1)
        self.pushButton_stop_writer.clicked.connect(self.stop_writer)

        self.pushButton_reader = QPushButton(self.centralwidget)
        self.pushButton_reader.setObjectName(u"pushButton_reader")
        self.gridLayout.addWidget(self.pushButton_reader, 2, 2, 1, 1)
        self.pushButton_reader.clicked.connect(self.run_reader)

        self.pushButton_stop_reader = QPushButton(self.centralwidget)
        self.pushButton_stop_reader.setObjectName(
            u"pushButton_stop_reader")
        self.gridLayout.addWidget(self.pushButton_stop_reader, 3, 2, 1, 1)
        self.pushButton_stop_reader.clicked.connect(self.stop_reader)

        # Set all widgets in the window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        """ Set text in widgets """
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Reader-Writer problem - AMR", None))
        self.label_reader.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso Lector", None))
        self.label_status.setText(QCoreApplication.translate(
            "MainWindow", u"Archivo inactivo", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"El Problema del Lector-Escritor", None))
        self.pushButton_writer.setText(
            QCoreApplication.translate("MainWindow", u"Escribir", None))
        self.pushButton_reader.setText(
            QCoreApplication.translate("MainWindow", u"Leer", None))
        self.label_writer.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso Escritor", None))
        self.pushButton_stop_reader.setText(
            QCoreApplication.translate("MainWindow", u"Detener", None))
        self.pushButton_stop_writer.setText(
            QCoreApplication.translate("MainWindow", u"Detener", None))
    # retranslateUi

    def run_writer(self) -> None:
        """ Create a writer process """
        self.pushButton_writer.setDisabled(True)
        self.pushButton_reader.setDisabled(True)
        self.pushButton_stop_reader.setDisabled(True)

        self.signal_writer = SignalProcess()
        self.writer = RunWriter(
            self.signal_writer, self.label_status)
        self.writer.signal.stopped.connect(self.stop_writer)

        self.thread_pool.start(self.writer)
    # run_writer

    def run_reader(self) -> None:
        """ Create a reader process """
        self.pushButton_writer.setDisabled(True)
        self.pushButton_reader.setDisabled(True)
        self.pushButton_stop_writer.setDisabled(True)

        self.signal_reader = SignalProcess()
        self.reader = RunReader(
            self.signal_reader, self.label_status)
        self.reader.signal.stopped.connect(self.stop_reader)

        self.thread_pool.start(self.reader)
    # run_reader

    def stop_writer(self) -> None:
        """ Stop the writer """
        self.writer.stop()
        self.pushButton_writer.setDisabled(False)
        self.pushButton_reader.setDisabled(False)
        self.pushButton_stop_reader.setDisabled(False)
    # stop_writer

    def stop_reader(self) -> None:
        """ Stop the reader """
        self.reader.stop()
        self.pushButton_writer.setDisabled(False)
        self.pushButton_reader.setDisabled(False)
        self.pushButton_stop_writer.setDisabled(False)
    # stop_reader
# ReaderWriterWindow


if __name__ == "__main__":
    app = QApplication([])
    window = ReaderWriterWindow()
    window.show()
    exit(app.exec())
